# PageDataLoadResult

## 基本信息

- **事件显示名**: 数据加载结果
- **事件英文名**: `PageDataLoadResult`
- **所属模块**: 0.全局埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 基本上所有页面 包括：首页，LP，分类，购物车，商品详情页，订单列表，售后单，售后单详情等 |  |  |  |  |  |  |
| `from_page` |  |  |  |  |  |  |  |
| `from_module` |  |  |  |  |  |  |  |
| `page_data_status` | 页面数据状态：-1: loading; 0:Failed; 1: Success | Int | 加载中-1， 没有数据0，有数据 >0 |  |  |  |  |
| `Result` | 页面状态描述 |  |  |  |  |  |  |
| `failure_cause` | 失败的原因 |  |  |  |  |  |  |
| `page_appear_count` | 页面曝光次数 | Int | 比如用户离开该页面再次返回 会累加1 |  |  |  |  |
| `page_appear_time` | 页面曝光时间 | Double(ms) | 当前事件距离页面曝光的时间间隔 |  |  |  |  |
