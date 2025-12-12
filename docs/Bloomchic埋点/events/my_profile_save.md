# my_profile_save

## 基本信息

- **事件显示名**: 个人资料保存My Profile页面
- **事件英文名**: `my_profile_save`
- **所属模块**: 6.【me页】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `email` | 登录用户email | STRING |  |  |  |  |  |
| `profile_result` | profile保存结果 | INT | 1是成功，0是失败 |  |  |  |  |
| `failed_reason` | 上传失败原因 | STRING | review_result为0上报具体内容，为1时上报空 |  |  |  |  |
