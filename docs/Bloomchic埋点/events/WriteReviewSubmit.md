# WriteReviewSubmit

## 基本信息

- **事件显示名**: 评论提交后上报：成功/失败
- **事件英文名**: `WriteReviewSubmit`
- **所属模块**: 6.【me页】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_from` | 页面来源：商详页/我的评论 | STRING |  |  |  | WriteReviews页面 |  |
| `order_id` | 订单ID，订单长 | STRING |  |  |  |  |  |
| `order` | 订单Num, 订单短码 | STRING |  |  |  |  |  |
| `product_sku` | 评论商品SKU | STRING |  |  |  |  |  |
| `product_spu` | 评论商品SPU | STRING |  |  |  |  |  |
| `product_name` | 商品名 | STRING |  |  |  |  |  |
| `review_result` | 评价上传结果 | STRING |  |  |  |  |  |
| `failed_reason` | 上传失败原因：成功时报"" | STRING |  |  |  |  |  |
| `overall_rating` | 综合评分 | NUMBER |  |  |  |  |  |
| `fit` | 合身度 | NUMBER |  |  |  |  |  |
| `review_content` | 评价内容 | STRING |  |  |  |  |  |
| `video_url` | 视频URL | STRING |  |  |  |  |  |
| `image_count` | 图片数量 | NUMBER |  |  |  |  |  |
| `Anonymous_type` | 是否匿名提交 | BOOLEAN |  |  |  |  |  |
| `publish_type` | 提交类型 | String | APP3.10新增属性值<br/>提交是是首次提交还是编辑提交，枚举项：<br/>- 新提交 ："new"<br/>- 编辑提交 :"edit" |  |  |  |  |
| `delivery_status` | 物流状态 | INT | 0=已签收；<br/>1=未签收； | APP3.6新增 |  |  |  |
