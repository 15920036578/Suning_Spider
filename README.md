# 苏宁爬虫
![](https://img.shields.io/badge/Python-3.5.3-green.svg) ![](https://img.shields.io/badge/Scrapy-1.5.1-green.svg)
#### 苏宁官网 - https://www.suning.com/
|Author|Gobi Xu|
|---|---|
|Email|xusanity@aliyun.com|
****
## 声明
#### 任何内容都仅用于学习交流，请勿用于任何商业用途。
## 前言
#### 简单说明
- **请求时不需要携带cookies（即不需要先登录），过程相对轻松**
- **需要爬取的数据通过请求地址携带参数即可得到**
## 运行环境
#### Version: Python3
## 安装依赖库
```
pip install scrapy
```
## 细节
- **商品列表页后半部分是异步加载的**
###### 每页分为4层，直接请求商品列表页地址的话，只会显示第一层，其余3层是用户下拉后异步加载出来的，使用抓包的方法可以截取到，所以每一页都分为4步来分别请求
- **商品列表页后半部分是异步加载的**
###### 商品列表页一共有50页，请求地址参数中的cp为页数（0~49），paging为层数（0~3）
## 类目
#### :telephone_receiver:[手机](https://search.suning.com/%E6%89%8B%E6%9C%BA/)
#### 爬取字段：
- **商品id (id)**
- **商品标题 (title)**
- **商品价格 (price)**
- **商品牌子 (brand)**
- **商品型号 (model)**
- **商品的网店名称 (shop_name)**
- **商品评论数量 (comment_count)**
- **商品详情页网址 (url)**
## 最后
- **对应的spider里有大量注释，请放心食用:meat_on_bone:**
- **对应的类目在items.py里**
- **如有任何问题都可以邮箱:email:联系我，我会尽快回复你。**
