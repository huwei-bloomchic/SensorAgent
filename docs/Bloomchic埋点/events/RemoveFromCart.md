# RemoveFromCart

## 基本信息

- **事件显示名**: 点击【delete】<br/>按照商品维度单个上报
- **事件英文名**: `RemoveFromCart`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,iOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `reason` | 来源 | STRING | 修改SKU:"Modify sku"<br/>删除商品:"Delete"<br/>移到心愿单:"Move to wishlist"<br/>购买成功:"Purchase"<br/>删除原因新增以下：<br/>购物车按钮删除<br/>长按删除<br/>移除失效模块<br/>编辑删除全部按钮 | 原APP2.14埋点<br/>APP3.6新增类型 |  | 购物车&购物车编辑 |  |
| `product_spu` | 商品SPU | STRING |  |  |  |  |  |
| `product_sku` | 商品SKU | STRING |  |  |  |  |  |
| `product_id` | Shopify Product ID | STRING |  |  |  |  |  |
| `web_original_price` | NUMBER | 原价 |  |  |  |  |  |
| `web_current_price` | NUMBER | 价格 |  |  |  |  |  |
| `web_discount_price` | NUMBER | 折扣 |  |  |  |  |  |
| `product_name` | STRING | 商品名称 | 商品名称 |  |  |  |  |
| `sku_status` | SKU状态 | STRING | 【SKU在售】：库存>0，或缺货在售<br/>【SKU下架】：sku库存为0且没缺货在售，但SPU其他商品还在售；或者这个SPU在架但SKU是下架状态，<br/>【SPU下架】：spu下架 | APP3.6新增 |  |  |  |
