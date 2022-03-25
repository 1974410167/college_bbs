- pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
- python manage.py makemigrations
- python manage.py migrate
- celery -A college_bbs beat   # 发布任务
- celery -A college_bbs worker --loglevel=info # 执行任务

管理员账号：hyuan 
密码：123456
> 一个架构合理，代码优美，高性能的校园论坛系统


