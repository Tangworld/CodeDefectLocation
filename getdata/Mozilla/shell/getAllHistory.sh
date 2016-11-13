#循环遍历/home/tsj/PycharmProjects/gecko-dev目录下的所有子孙目录中的文件，将其复制到/home/tsj/PycharmProjects/latest目录中
#同时执行git命令，获取git log，并将得到的信息重定向到/home/tsj/PycharmProjects/history/目录下，文件命名为原本文件名加上txt后缀
#如Main.java对应的history文件命名为Main.java.txt

#!/bin/bash  
list_alldir(){  
for file2 in `ls -a $1`  # $1 执行该脚本时输入的第一个参数，首先列出该目录下的全部文件（夹），然后用for循环遍历
do                       # for循环的循环体
    if [ x"$file2" != x"." -a x"$file2" != x".." ];then  #如果不是./..
        if [ -d "$1/$file2" ];then                       #如果$1/$file2是目录
            list_alldir "$1/$file2"                      #递归调用，进入该目录
	    else                                             #如果是文件
	      if [ -f"$file2" ]; then
              sudo cp $1/$file2 /home/tsj/PycharmProjects/latest                       #文件复制
              git log -p $1/$file2 > /home/tsj/PycharmProjects/history/$file2.txt     #执行git log 并将结果重定向到txt文件中
	       fi
        fi  
    fi  
done                     # 循环体结束
}  

list_alldir /home/tsj/PycharmProjects/gecko-dev
