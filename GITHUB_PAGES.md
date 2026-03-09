# GitHub Pages 部署指南

本文档说明如何将提示词生成器部署到 GitHub Pages。

---

## 🚀 快速部署

### 方式一：使用 GitHub Actions（推荐）

已创建自动化部署配置，推送后自动部署。

#### 步骤

1. **推送代码到 GitHub**

2. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"

3. **等待部署完成**
   - 访问：`https://<username>.github.io/astrbot_plugin_dev_guide/`

---

### 方式二：手动配置

#### 步骤 1：启用 GitHub Pages

1. 打开仓库：https://github.com/86lbs/astrbot_plugin_dev_guide
2. 点击 **Settings** 标签
3. 左侧菜单找到 **Pages**
4. **Source** 选择：
   - `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
5. 点击 **Save**

#### 步骤 2：等待部署

- GitHub 会自动构建
- 几分钟后可访问：`https://86lbs.github.io/astrbot_plugin_dev_guide/`

---

## 📁 文件结构要求

GitHub Pages 需要以下文件在仓库根目录：

```
astrbot_plugin_dev_guide/
├── index.html              # 首页（需要创建）
├── prompt_generator.html   # 提示词生成器
├── README.md
└── ...
```

---

## 🔧 创建首页重定向

为了让 `https://86lbs.github.io/astrbot_plugin_dev_guide/` 直接显示提示词生成器：

---

## 📊 访问地址

部署成功后：

| 页面 | 地址 |
|------|------|
| 首页 | `https://86lbs.github.io/astrbot_plugin_dev_guide/` |
| 提示词生成器 | `https://86lbs.github.io/astrbot_plugin_dev_guide/prompt_generator.html` |
| README | `https://86lbs.github.io/astrbot_plugin_dev_guide/README.md` |

---

## ⚠️ 注意事项

1. **首次部署**：可能需要等待 1-5 分钟
2. **更新后**：推送新代码后自动更新
3. **自定义域名**：可在 Pages 设置中配置
4. **HTTPS**：GitHub Pages 默认启用 HTTPS

---

## 🔗 相关链接

- [GitHub Pages 官方文档](https://docs.github.com/en/pages)
- [GitHub Pages 快速入门](https://docs.github.com/en/pages/quickstart)
