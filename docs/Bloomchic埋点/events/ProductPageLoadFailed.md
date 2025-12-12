# ProductPageLoadFailed

## 基本信息

- **事件显示名**: 商品加载失败
- **事件英文名**: `ProductPageLoadFailed`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_id` | 商品ID | STRING |  |  |  |  |  |
| `product_handle` | 商品handle | STRING |  |  |  |  |  |
| `failed_reason` | 加载失败的原因 | STRING | ""：没有推荐,上报空字符串<br/>23-23/2L |  |  |  |  |
