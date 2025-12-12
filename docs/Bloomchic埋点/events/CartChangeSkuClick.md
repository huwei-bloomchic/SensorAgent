# CartChangeSkuClick

## 基本信息

- **事件显示名**: 点击商品的换尺码
- **事件英文名**: `CartChangeSkuClick`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,iOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING |  | APP3.6新增 |  | 购物车 |  |
| `product_sku` | 商品SKU | STRING |  | APP3.6新增 |  |  |  |
| `product_id` | Shopify Product ID | STRING |  | APP3.6新增 |  |  |  |
| `sku_status` | SKU状态 | STRING | 【SKU在售】：库存>0，或缺货在售<br/>【SKU下架】：sku库存为0且没缺货在售，但SPU其他商品还在售；或者这个SPU在架但SKU是下架状态，<br/>【SPU下架】：spu下架 | APP3.6新增 |  |  |  |
