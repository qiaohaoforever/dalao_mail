#代理
export http_proxy=http://xx.xx.xxx:xxxx
export https_proxy=http://xx.xx.xxx:xxxx


yesterday=`date -d "yesterday" +%Y-%m-%d`
echo $yesterday
#spark-sql执行对应sql，3个sheet
#attach
spark-sql -hiveconf dt="$yesterday" --conf spark.executor.memory=32g --conf spark.executor.cores=8 --conf spark.cores.max=40 -f a.sql
spark-sql -hiveconf dt="$yesterday" --conf spark.executor.memory=32g --conf spark.executor.cores=8 --conf spark.cores.max=40 -f b.sql | grep -v 'ERROR' | tr "\t" "," > b.csv
spark-sql -hiveconf dt="$yesterday" --conf spark.executor.memory=32g --conf spark.executor.cores=8 --conf spark.cores.max=40 -f c.sql | grep -v 'ERROR' | tr "\t" "," > c.csv

#csv to html attach
csvtotable b.csv b.html
csvtotable c.csv c.html

#python 将三个sheet组合成1个Excel，并发送
python -u send_mail.py $yesterday

#删除历史数据
rm b.csv b.html c.csv c.html
echo "$yesterday 日报发送完毕！"
