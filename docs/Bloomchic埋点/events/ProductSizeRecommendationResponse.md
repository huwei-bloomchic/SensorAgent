# ProductSizeRecommendationResponse

## 基本信息

- **事件显示名**: 商品尺码接口响应<br/>在服务端返回的need_ab_test = true才上报
- **事件英文名**: `ProductSizeRecommendationResponse`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING |  |  |  |  |  |
| `product_id` | 商品ID | STRING |  |  |  |  |  |
| `recommended_type` | 1: 推荐成功2: 引导用户填写尺码3:推荐失败 | STRING |  |  |  |  |  |
| `recommended_describe` | 推荐的描述 | STRING |  |  |  |  |  |
| `recommended_size` | 推荐的尺码，虚拟字段：combine_recommend_size | STRING |  |  |  |  |  |
