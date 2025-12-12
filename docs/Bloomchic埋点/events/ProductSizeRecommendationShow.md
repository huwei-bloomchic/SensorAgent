# ProductSizeRecommendationShow

## 基本信息

- **事件显示名**: 商品尺码推荐展示
- **事件英文名**: `ProductSizeRecommendationShow`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING |  | 商详页-尺码推荐模块展示的曝光 |  |  |  |
| `product_id` | 商品ID | STRING |  |  |  |  |  |
| `recommended_size` | 推荐的尺码虚拟字段：combine_recommend_size | STRING | ""：没有推荐,上报空字符串<br/>23-23/2L |  |  |  |  |
