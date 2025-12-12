# CheckoutCreateFailed

## 基本信息

- **事件显示名**: Checkout接口请求失败
- **事件英文名**: `CheckoutCreateFailed`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,iOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cart_type` | 固定值：完整购物车 | String |  |  |  |  |  |
| `product_quantity` | 参照CheckoutStart埋点 | Int |  |  |  |  |  |
| `product_spu_list` |  | String |  |  |  |  |  |
| `product_sku_list` |  | String |  |  |  |  |  |
| `subtotal` |  | DOUBLE |  |  |  |  |  |
| `product_id` |  | String |  |  |  |  |  |
| `failed_reason` |  | String |  |  |  |  |  |
