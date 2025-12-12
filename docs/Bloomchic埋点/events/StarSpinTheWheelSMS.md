# StarSpinTheWheelSMS

## 基本信息

- **事件显示名**: SMS步骤点击抽奖
- **事件英文名**: `StarSpinTheWheelSMS`
- **所属模块**: 1.【首页】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 | JavaScript | 点击spin the wheel、wheel of luck时上报 | 几个实验组都需要更改 |  |
| `popup_type` | 弹窗类型 | INT | 7=带转盘前置弹窗版本（V1.2） | JavaScript |  |  |  |
| `click_item` | 点击位置 | STRING | 1=Span the wheel<br/>2=Wheel of Luck（转盘指针） | JavaScript |  |  |  |
| `email_content` | 订阅邮箱 | STRING | 用户在邮箱框输入的内容 |  |  |  |  |
| `sms_content` | 手机号 | STRING | 用户在sms框输入的内容 |  |  | 2024-6月5日新增 |  |
| `check_result` | 手机号校验结果 | INT | 1=通过<br/>2=格式不正确<br/>3=非新用户 |  |  | 2024-6月5日新增 |  |
