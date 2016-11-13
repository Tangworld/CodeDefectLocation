#循环遍历/home/tsj/IdeaProjects/org.aspectj目录下的所有子孙目录中的java文件，将其复制到/home/tsj/IdeaProjects/latest目录中
#同时执行git命令，获取git log，并将得到的信息重定向到/home/tsj/IdeaProjects/history/目录下，文件命名为原本文件名加上txt后缀
#如Main.java对应的history文件命名为Main.java.txt

#!/bin/bash  
list_alldir(){  
for file2 in `ls -a $1`  
do  
    if [ x"$file2" != x"." -a x"$file2" != x".." ];then  
        if [ -d "$1/$file2" ];then   
            list_alldir "$1/$file2"  
	    else 
	       if [ "${file2##*.}" = "java" ]; then
		  sudo cp $1/$file2 /home/tsj/IdeaProjects/latest
		  git log -p $1/$file2 > /home/tsj/IdeaProjects/history/$file2.txt
	       fi
        fi  
    fi  
done  
}  

list_alldir /home/tsj/IdeaProjects/org.aspectj
