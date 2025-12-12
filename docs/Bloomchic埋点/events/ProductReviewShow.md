# ProductReviewShow

## 基本信息

- **事件显示名**: 商详评论展示/评论列表中 评论展示<br/>（单条评论维度的商上报，展示1条上报1次）
- **事件英文名**: `ProductReviewShow`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_from_page` | 商品来源页面 | STRING | 首页-Just dropped、首页-Best sellers、商品列表-ID、You may also like、 Customer Also Bought、搜索结果页 | JavaScript | 进入当前商详页之后，在此商详页只上报一次<br/>商详滑动此模块时上报，包含评论总评分星级模块和商详展示的用户模块内容。 |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 |  |  |  |  |
| `product_id` | 商品ID |  |  |  |  |  |  |
| `product_name` | 商品名称 | STRING |  |  |  |  |  |
| `review_id` | 评论ID | INT | 详情页没有评论则不上报 |  |  |  |  |
| `review_number` | 评价数量 | INT | 1) 通过审核的评价总数(人工审核、自动审核)：0、1、2、3...<br/>2) 当没有评价时，此时数量取0 |  |  |  |  |
| `average_overall_rating` | 综合评分均值 | NUMBER | 1) 取综合评分均值，小数点后一位：1、1.1、1.2...2.1、2.2...4.9、5<br/>2) 当评价数量为0时，此时的综合评分为0 |  |  |  |  |
| `overall_rating` | 综合评分 | INT | 1、2、3、4、5 |  |  |  |  |
| `fit` | 合身度 | STRING | True To Size、Small、Large |  |  |  |  |
| `review_content` | 评价内容 | STRING | 用户具体填写内容 |  |  |  |  |
| `photo_number` | 图片数量 | INT | 1、2... |  |  |  |  |
| `name_content` | 姓名内容 | STRING | 用户评论姓名 |  |  |  |  |
