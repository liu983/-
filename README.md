项目一：获取广东省人民政府办公厅特定日期间的政策数据
  
  功能：
  
      a.收集索引号、发布机构、发布日期、政策标题、政策正文文本、政策正文附件链接，以上六项信息
      b.收集特定时间区间内的全部政策信息
      
  说明：
  
      使用lxml库做页面解析
      
  使用：
  
      输入：日期范围		例：(20220101-20230601)
	    输出：指定时间范围内的全部政策信息

  环境：
  
      ide:pycharm,python3.7
      库：requests,lxml,time,json,random,datetime


项目二：获取天眼查平台某家公司的全部专利数据
  
  功能：
  
      a.完成自动登录并获取Cookie
      b.获取任意一家企业的全部专利数据
      
  说明：
  
      selenium库完成账号登录
      
  使用：
  
      输入：企业名称		例：(华为技术有限公司)
	    输出：指定企业的全部专利数据列表

  环境：
  
      ide:pycharm,python3.7
      库：seleium,chajiying,time
