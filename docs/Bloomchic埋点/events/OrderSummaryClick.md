# OrderSummaryClick

## 基本信息

- **事件显示名**: 点击Order summary
- **事件英文名**: `OrderSummaryClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_name` | 所在页面名称 | STRING | Information、Shipping、Payment | JavaScript | 点击Order summary时上报，包括展开和收起 | 9月29日23: 30 新增 |  |
| `click_type` | 点击后展开或收起 | INT | 点击后show order summary的状态，比如点击后状态为展开则报1<br/>1=展开<br/>2=收起 | JavaScript |  |  |  |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 | JavaScript |  |  |  |
| `product_spu_list` | 商品SPU列表 | STRING | SPU1;SPU2;SPU3;.......... | JavaScript |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING | SKU1;SKU2;SKU3;.......... | JavaScript |  |  |  |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 | JavaScript |  |  |  |
| `discount` | 订单折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `shipping` | 运费金额 | NUMBER |  | JavaScript |  |  |  |
| `total` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
