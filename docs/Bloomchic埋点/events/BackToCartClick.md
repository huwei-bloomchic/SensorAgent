# BackToCartClick

## 基本信息

- **事件显示名**: 点击Back to cart
- **事件英文名**: `BackToCartClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 | JavaScript | 点击Back to cart按钮时上报 | 9月29日23: 30 新增 |  |
| `product_spu_list` | 商品SPU列表 | STRING | SPU1;SPU2;SPU3;.......... | JavaScript |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING | SKU1;SKU2;SKU3;.......... | JavaScript |  |  |  |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 | JavaScript |  |  |  |
| `discount` | 订单折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `shipping` | 运费金额 | NUMBER |  | JavaScript |  |  |  |
| `total` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
