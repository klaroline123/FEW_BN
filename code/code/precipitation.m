clear
clc

% ����ѭ����ȡ����tiff�ļ�
namelist=[1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018];
for i=1:length(namelist)
    str=num2str(namelist(i));
    file_path = 'E:\precipitation\';% ͼ���ļ���·�� 
    img_path_list = dir(strcat(file_path,'*',str,'*.tif'));%��ȡ���ļ���������TIF��ʽ��ͼ��
    img_num = length(img_path_list);%��ȡͼ��������
    II=cell(1,img_num);
    for jj=1:img_num
        image_name = img_path_list(jj).name;% ͼ���� 
        [image,geo] = geotiffread(strcat(file_path,image_name)); 
        info=geotiffread(strcat(file_path,image_name));
        II{jj}=image;
        image=double(image);

%imgray=rgb2gray(im);
        if jj==1
%         image_mean=zeros(size(image));%���ֻ��һ��ͼ�񣬾�ֵΪ��ͼ���ֵ
            image_sum=zeros(size(image));
        end
%     image_mean=image_mean+image/img_num;
        image_sum=image_sum+image;
    end
image_sum=single(image_sum);
image_sum_name=strcat(file_path,str,'.tif');
geotiffwrite(image_sum_name,image_sum,geo);    
end
