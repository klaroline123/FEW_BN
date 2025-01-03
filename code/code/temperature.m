clear
clc

filename ='E:\temperature\country1.txt';                      %�ļ���
delimiterIn = ' ';                          %�зָ���
headerlinesIn =6;                           %��ȡ�ӵ� headerlinesIn+1 �п�ʼ����ֵ����
temp=importdata(filename,delimiterIn,headerlinesIn);
dataset=temp.data;
m=length(dataset);  
n=fix(m/12);%nΪ����ϵ�г��ȣ��������ݼ�����12
year_value_set=zeros(n,2);
ave_temp=dlmread(filename,'',[2 1 2 12]);
for i=1:n %1��m����Ϊ12
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