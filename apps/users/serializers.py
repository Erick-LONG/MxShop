import re
from datetime import datetime,timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from MxShop.settings import MOBILE_RE
from .models import VerifyCode

User = get_user_model()


#因为前端没有给传code，所以用Serializer
class SmsSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self,mobile):
        '''验证手机号码'''

        #手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        #验证手机号码是否合法
        if not re.match(MOBILE_RE,mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证发送频率
        one_mintes_ago = datetime.now()- timedelta(hours=0,minutes=1,seconds = 0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True,write_only=True,label='验证码',max_length=4,min_length=4,error_messages={
                                                                        'blank':'请输入验证码',
                                                                        'required':'请输入验证码',
                                                                        'max_length':'验证码格式错误',
                                                                        'min_length': '验证码格式错误',
                                                                    },help_text='验证码')
    username = serializers.CharField(label='用户名',required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),message='用戶已經存在') ])

    #write_only设置为只写
    password = serializers.CharField(
        style={'input_type':'password'},label='密码',write_only=True,
    )

    #加密保存密码
    # def create(self, validated_data):
    #     user = super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_record = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_record:
            last_record = verify_record[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    #作用于所有serializer字段之上，attrs返回所有字段的字典
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username','code','mobile','password')