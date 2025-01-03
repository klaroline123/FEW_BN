clear
clc

filename ='E:\temperature\country1.txt';                      %文件名
delimiterIn = ' ';                          %列分隔符
headerlinesIn =6;                           %读取从第 headerlinesIn+1 行开始的数值数据
temp=importdata(filename,delimiterIn,headerlinesIn);
dataset=temp.data;
m=length(dataset);  
n=fix(m/12);%n为数据系列长度，整个数据集整除12
year_value_set=zeros(n,2);
ave_temp=dlmread(filename,'',[2 1 2 12]);
for i=1:n %1到m步长为12
    for j=1:12
        value_location=(i-1)*12+j;
        month_value(j)=dataset(value_location,3)+ave_temp(j);
        year_value=mean(month_value);
    end
    year=dataset(value_location,1);
    year_value_set(i,1)=year;
    year_value_set(i,2)= year_value;
end   
  xlswrite('E:\temperature\country1_temp.xls', year_value_set);  