# GitHub项目上传详细指南

## 适合人群：GitHub完全新手

本指南将教会你如何将当前的视频处理工具项目上传到GitHub，拥有自己的第一个GitHub作品！

## 一、准备工作

### 1. 注册GitHub账号

1. 访问 GitHub 官网：https://github.com/
2. 点击右上角的「Sign up」按钮
3. 填写注册信息：
   - 用户名：建议使用容易记住且专业的名字
   - 邮箱：用于接收GitHub通知
   - 密码：建议使用强密码
4. 完成验证，注册成功后登录

### 2. 安装Git

Git是GitHub的本地客户端，用于管理代码版本和推送代码到GitHub。

1. 下载Git：https://git-scm.com/download/win
2. 安装Git：
   - 一路点击「Next」，使用默认设置即可
   - 注意：在「Select Components」步骤，确保勾选了「Git Bash Here」
   - 安装完成后，在任意文件夹右键，应该能看到「Git Bash Here」选项

## 二、创建GitHub仓库

1. 登录GitHub后，点击右上角的「+」号，选择「New repository」
2. 填写仓库信息：
   - **Repository name**：项目名称，建议使用英文，如「video-frame-extractor-grid-synthesizer」
   - **Description**：项目描述，如「A tool for extracting keyframes from videos and synthesizing them into grid images」
   - **Visibility**：选择「Public」（公开）或「Private」（私有），新手建议选择「Public」
   - **Initialize this repository with**：不要勾选任何选项，我们将手动初始化
3. 点击「Create repository」按钮，创建仓库

## 三、本地仓库配置

### 1. 初始化本地Git仓库

1. 打开「文件资源管理器」，进入项目根目录：`d:\2512201334-traeprojects\2601021230-视频处理工具`
2. 右键点击空白处，选择「Git Bash Here」，打开Git命令行
3. 初始化Git仓库：
   ```bash
   git init
   ```
   执行后，项目目录中会出现一个隐藏的 `.git` 文件夹

### 2. 配置Git用户名和邮箱

在Git Bash中执行以下命令：

```bash
# 替换为你的GitHub用户名
git config --global user.name "你的GitHub用户名"

# 替换为你的GitHub邮箱
git config --global user.email "你的GitHub邮箱"
```

### 3. 创建.gitignore文件

.gitignore文件用于告诉Git哪些文件不需要上传到GitHub，如编译文件、临时文件、虚拟环境等。

1. 在项目根目录创建 `.gitignore` 文件
2. 编辑 `.gitignore` 文件，添加以下内容：
   ```
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   
   # Virtual Environment
   venv/
   env/
   
   # IDE
   .vscode/
   *.swp
   *.swo
   *~
   
   # Logs
   logs/
   *.log
   
   # Output
   output/
   test_output/
   
   # Windows
   Thumbs.db
   
   # OS X
   .DS_Store
   
   # Other
   *.bak
   *.tmp
   ```
3. 保存文件

### 4. 完善README.md文件

README.md是项目的介绍文档，GitHub会自动显示在仓库首页。

1. 编辑项目根目录下的 `README.md` 文件
2. 确保包含以下内容：
   - 项目名称和简介
   - 功能特点
   - 环境要求
   - 安装步骤
   - 使用方法
   - 项目结构
   - 许可证

## 四、提交代码到本地仓库

1. 在Git Bash中，将所有文件添加到暂存区：
   ```bash
   git add .
   ```
   注意：`.` 表示当前目录下的所有文件

2. 提交代码到本地仓库：
   ```bash
   git commit -m "Initial commit - 视频关键帧提取与宫格合成工具"
   ```
   - `-m` 表示提交信息
   - 提交信息要清晰描述本次提交的内容

## 五、关联并推送代码到GitHub

### 1. 获取GitHub仓库的远程URL

1. 打开GitHub上刚创建的仓库页面
2. 点击绿色的「Code」按钮
3. 复制「HTTPS」或「SSH」URL，建议新手使用「HTTPS」URL
   - 示例：`https://github.com/你的用户名/你的仓库名.git`

### 2. 关联远程仓库

在Git Bash中执行：

```bash
git remote add origin 你的GitHub仓库URL
```

例如：
```bash
git remote add origin https://github.com/username/video-frame-extractor.git
```

### 3. 推送代码到GitHub

执行以下命令将本地代码推送到GitHub：

```bash
git push -u origin master
```

- `-u` 表示设置上游分支，后续推送可以直接使用 `git push`
- `origin` 是远程仓库的名称
- `master` 是分支名称（GitHub现在默认分支是 `main`，但有些旧版本使用 `master`）

### 4. 首次推送可能遇到的问题

- **用户名密码验证**：
  - 首次推送会要求输入GitHub用户名和密码
  - 注意：现在GitHub不再支持密码登录，需要使用**Personal Access Token**
  - 解决方案：在GitHub上生成Personal Access Token，然后在提示输入密码时输入Token

- **分支名称不匹配**：
  - 如果GitHub默认分支是 `main`，而本地是 `master`
  - 解决方案：将本地分支重命名为 `main`：
    ```bash
    git branch -M main
    git push -u origin main
    ```

## 六、生成Personal Access Token

如果遇到GitHub密码验证失败，需要生成Personal Access Token：

1. 登录GitHub，点击右上角头像 → 「Settings」
2. 左侧菜单选择「Developer settings」→ 「Personal access tokens」→ 「Tokens (classic)」
3. 点击「Generate new token」→ 「Generate new token (classic)」
4. 填写信息：
   - **Note**：Token名称，如「GitHub Token」
   - **Expiration**：Token有效期，建议选择「No expiration」
   - **Select scopes**：勾选「repo」（所有repo权限）
5. 点击「Generate token」
6. **重要**：复制生成的Token，这是你唯一一次看到它的机会！

使用方法：在Git Bash提示输入密码时，粘贴刚才复制的Token

## 七、验证上传结果

1. 刷新GitHub仓库页面
2. 你应该能看到项目的所有文件已经上传到GitHub
3. 检查README.md是否正常显示
4. 检查.gitignore是否生效，不必要的文件（如venv/、__pycache__/）是否没有上传

## 八、后续维护和更新

当你对项目进行修改后，需要更新GitHub上的代码：

1. 添加修改后的文件到暂存区：
   ```bash
   git add .
   ```

2. 提交到本地仓库：
   ```bash
   git commit -m "修改描述"
   ```

3. 推送到GitHub：
   ```bash
   git push
   ```

## 九、GitHub项目美化建议

1. **添加徽章**：在README.md中添加构建状态、许可证等徽章
2. **发布Release**：当项目达到一定成熟度时，可以发布正式版本
3. **添加贡献指南**：鼓励其他开发者贡献代码
4. **定期更新**：保持项目活跃，定期修复bug和添加新功能

## 十、常见问题和解决方案

1. **Git命令找不到**：
   - 确保Git已正确安装
   - 确保Git的安装路径已添加到系统PATH
   - 尝试使用「Git Bash」而不是「CMD」

2. **推送失败**：
   - 检查网络连接
   - 检查GitHub仓库URL是否正确
   - 检查Personal Access Token是否有效
   - 检查分支名称是否匹配

3. **文件没有上传**：
   - 确保执行了 `git add .` 和 `git commit` 命令
   - 检查 `.gitignore` 文件是否误将需要上传的文件排除

## 十一、学习资源

- GitHub官方文档：https://docs.github.com/zh
- Git官方教程：https://git-scm.com/book/zh/v2
- GitHub入门教程：https://guides.github.com/activities/hello-world/

## 总结

上传项目到GitHub是一个很好的学习过程，从不会到会需要一些时间和实践。遇到问题是正常的，通过搜索引擎和GitHub文档，你可以解决大部分问题。

记住：
- 这是一个学习过程，不要害怕犯错
- 定期备份代码到GitHub，养成良好的版本控制习惯
- 编写好的README.md，让别人更容易理解和使用你的项目
- 持续维护和更新，让你的项目变得更好

祝你成功拥有第一个GitHub作品！🚀