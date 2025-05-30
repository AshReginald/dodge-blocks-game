# dodge-blocks-game
# 🚧 Dodge Blocks Game

Một trò chơi web hiện đại được phát triển bằng Next.js, TypeScript và HTML5 Canvas. Người chơi điều khiển một khối vuông để tránh các khối rơi từ trên xuống, với nhiều power-ups và sự kiện đặc biệt thú vị.

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt từ đầu](#-cài-đặt-từ-đầu)
- [Cách chạy game](#-cách-chạy-game)
- [Cách chơi](#-cách-chơi)
- [Kiến trúc code](#-kiến-trúc-code)
- [Tùy chỉnh và mở rộng](#-tùy-chỉnh-và-mở-rộng)

## 🎮 Tính năng

### Gameplay cơ bản
- **Điều khiển mượt mà**: Sử dụng phím mũi tên hoặc WASD
- **Hệ thống điểm số**: Tích lũy điểm khi tránh được khối
- **Level progression**: Độ khó tăng dần theo thời gian
- **High score**: Lưu điểm cao nhất vào localStorage

### Power-ups
- **🛡️ Shield**: Bảo vệ khỏi va chạm trong 5 giây
- **⚡ Speed Boost**: Tăng tốc độ di chuyển trong 5 giây  
- **⭐ Score Bonus**: Cộng ngay 50 điểm

### 18 Sự kiện đặc biệt
1. **BIG_BLOCKS** - Khối lớn hơn bình thường
2. **TINY_BLOCKS** - Khối nhỏ hơn, khó nhìn
3. **FAST_BLOCKS** - Tốc độ rơi tăng, điểm x3
4. **SLOW_MOTION** - Mọi thứ chậm lại
5. **MIRROR_MODE** - Đảo ngược điều khiển
6. **BLOCK_RAIN** - Mưa khối dày đặc
7. **GHOST_BLOCKS** - Một số khối trở nên trong suốt
8. **COLOR_CHANGE** - Đổi màu nền ngẫu nhiên
9. **GRAVITY_FLIP** - Khối bay lên thay vì rơi xuống
10. **MAGNET_PULL** - Khối bị hút về phía người chơi
11. **INVISIBLE_PLAYER** - Người chơi trở nên mờ
12. **DOUBLE_SCORE** - Điểm số x4
13. **FREEZE_BLOCKS** - Tất cả khối đứng yên
14. **SPIRAL_BLOCKS** - Khối di chuyển theo hình xoắn ốc
15. **EARTHQUAKE** - Màn hình rung lắc
16. **LASER_BEAM** - Tia laser ngang cần tránh
17. **SHIELD_RAIN** - Mưa shield power-ups
18. **TELEPORT_BLOCKS** - Khối dịch chuyển ngẫu nhiên

### Giao diện và UX
- **Responsive design**: Tối ưu cho mọi thiết bị
- **Dark theme**: Giao diện tối hiện đại
- **Particle effects**: Hiệu ứng hạt khi thu thập power-ups
- **Sound system**: Âm thanh cho mọi hành động
- **Menu system**: Main menu, instructions, game over

## 📁 Cấu trúc thư mục

```
dodge-blocks-game/
├── app/                          # Next.js App Router
│   ├── globals.css              # CSS toàn cục, Tailwind styles
│   ├── layout.tsx               # Layout chính của ứng dụng
│   └── page.tsx                 # Trang chính, quản lý state game
├── components/                   # React Components
│   ├── ui/                      # shadcn/ui components (tự động)
│   │   ├── button.tsx           # Component nút bấm
│   │   └── card.tsx             # Component thẻ
│   ├── game-canvas.tsx          # Component game chính (Canvas)
│   ├── game-over.tsx            # Màn hình game over
│   ├── instructions.tsx         # Hướng dẫn chơi
│   └── main-menu.tsx            # Menu chính
├── lib/                         # Utilities
│   └── utils.ts                 # Hàm tiện ích (cn function)
├── public/                      # Static files
├── .eslintrc.json              # ESLint configuration
├── .gitignore                  # Git ignore rules
├── components.json             # shadcn/ui configuration
├── dodge_game(origin file)     # file python phiên bản nguyên thuỷ của trò chơi
├── dodge_blocks_game           # file python trò chơi, đọc để hiểu ý tưởng và logic game
├── next.config.mjs             # Next.js configuration
├── package.json                # Dependencies và scripts
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── README.md                   # File này
```

## 🔧 Yêu cầu hệ thống

### Phần mềm cần thiết:
- **Node.js**: Phiên bản 18.0 trở lên
- **npm**: Đi kèm với Node.js (hoặc yarn, pnpm)
- **Git**: Để clone repository
- **Trình duyệt web**: Chrome, Firefox, Safari, Edge (hỗ trợ HTML5 Canvas)

### Hệ điều hành:
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 18.04+, CentOS 7+)

## 🚀 Cài đặt từ đầu

### Bước 1: Cài đặt Node.js

#### Windows:
1. Truy cập [nodejs.org](https://nodejs.org/)
2. Tải phiên bản LTS (Long Term Support)
3. Chạy file .msi và làm theo hướng dẫn
4. Mở Command Prompt và kiểm tra:
   ```cmd
   node --version
   npm --version
   ```

#### macOS:
1. Sử dụng Homebrew (khuyến nghị):
   ```bash
   # Cài đặt Homebrew nếu chưa có
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Cài đặt Node.js
   brew install node
   ```

2. Hoặc tải từ [nodejs.org](https://nodejs.org/)

#### Linux (Ubuntu/Debian):
```bash
# Cập nhật package list
sudo apt update

# Cài đặt Node.js và npm
sudo apt install nodejs npm

# Kiểm tra phiên bản
node --version
npm --version
```

### Bước 2: Cài đặt Git

#### Windows:
1. Tải Git từ [git-scm.com](https://git-scm.com/)
2. Cài đặt với các tùy chọn mặc định

#### macOS:
```bash
# Sử dụng Homebrew
brew install git

# Hoặc cài đặt Xcode Command Line Tools
xcode-select --install
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL
sudo yum install git
```

### Bước 3: Clone và cài đặt project

```bash
# Clone repository (thay YOUR_REPO_URL bằng URL thực tế)
git clone YOUR_REPO_URL
cd dodge-blocks-game

# Cài đặt dependencies
npm install

# Hoặc sử dụng yarn
yarn install

# Hoặc sử dụng pnpm
pnpm install
```

## 🎯 Cách chạy game

### Development mode (Phát triển):
```bash
# Chạy server development
npm run dev

# Hoặc
yarn dev

# Hoặc
pnpm dev
```

Mở trình duyệt và truy cập: `http://localhost:3000`

### Production build (Sản xuất):
```bash
# Build ứng dụng
npm run build

# Chạy production server
npm start
```

### Các lệnh khác:
```bash
# Kiểm tra lỗi code
npm run lint

# Tự động sửa lỗi lint
npm run lint:fix

# Type checking
npm run type-check
```

Đối với file python game:
# Cài đặt pygame nếu chưa có
pip install pygame

# Chạy game
python dodge_game_enhanced.py
(hoặc) python dodge_game.py

## 🎮 Cách chơi

### Điều khiển cơ bản:
- **← →** hoặc **A D**: Di chuyển trái/phải
- **Space**: Tạm dừng/Tiếp tục game
- **R**: Chơi lại khi game over

### Mục tiêu:
1. Tránh các khối đỏ rơi từ trên xuống
2. Thu thập power-ups để có lợi thế
3. Sống sót qua các sự kiện đặc biệt
4. Đạt điểm số cao nhất có thể

### Chiến thuật:
- **Ưu tiên shield**: Power-up quan trọng nhất
- **Tận dụng speed boost**: Khi có nhiều khối
- **Chú ý warning**: Chuẩn bị cho sự kiện đặc biệt
- **Giữ bình tĩnh**: Trong các event khó như Mirror Mode

## 🏗️ Kiến trúc code

### Luồng dữ liệu:
```
app/page.tsx (Game State Management)
    ↓
components/main-menu.tsx (Menu)
components/game-canvas.tsx (Game Logic)
components/game-over.tsx (End Screen)
components/instructions.tsx (Help)
```

### Chi tiết từng file:

#### `app/page.tsx`
- **Chức năng**: Component chính, quản lý state toàn cục
- **State management**: gameState, gameStats, soundEnabled
- **Routing**: Điều hướng giữa các màn hình
- **Data persistence**: Lưu/đọc high score từ localStorage

#### `components/game-canvas.tsx`
- **Chức năng**: Game engine chính sử dụng HTML5 Canvas
- **Game loop**: requestAnimationFrame cho 60 FPS
- **Input handling**: Keyboard events với smooth movement
- **Collision detection**: AABB collision system
- **Event system**: 18 special events với logic riêng
- **Audio system**: Web Audio API cho sound effects
- **Particle system**: Visual effects cho power-ups

#### `components/main-menu.tsx`
- **Chức năng**: Màn hình menu chính
- **Features**: Start game, instructions, high score display
- **Styling**: Gradient design với shadcn/ui components

#### `components/game-over.tsx`
- **Chức năng**: Màn hình kết thúc game
- **Features**: Score display, new high score detection, restart/menu options

#### `components/instructions.tsx`
- **Chức năng**: Hướng dẫn chơi chi tiết
- **Content**: Controls, power-ups, events explanation

### Cấu trúc dữ liệu chính:

#### GameObject Interface:
```typescript
interface GameObject {
  x: number          // Vị trí X
  y: number          // Vị trí Y  
  width: number      // Chiều rộng
  height: number     // Chiều cao
  color: string      // Màu sắc
  speed?: number     // Tốc độ (optional)
}
```

#### Game State:
```typescript
interface GameState {
  player: GameObject           // Người chơi
  blocks: GameObject[]         // Mảng khối rơi
  powerUps: PowerUp[]         // Mảng power-ups
  particles: Particle[]       // Mảng hiệu ứng
  score: number               // Điểm số
  level: number               // Level hiện tại
  activeEvents: object        // Sự kiện đang hoạt động
  // ... các thuộc tính khác
}
```

### Game Loop Architecture:
```
requestAnimationFrame
    ↓
handleInput() - Xử lý input
    ↓
updateGame() - Cập nhật logic
    ↓
render() - Vẽ lên canvas
    ↓
Lặp lại...
```

## 🛠️ Tùy chỉnh và mở rộng

### Thêm Power-up mới:
1. Thêm type vào `PowerUp` interface
2. Thêm logic spawn trong `spawnPowerUp()`
3. Thêm xử lý collision trong `updateGame()`
4. Thêm visual trong `render()`

### Thêm Event mới:
1. Thêm tên event vào array trong `triggerEvent()`
2. Thêm logic kích hoạt trong switch case
3. Thêm logic kết thúc event
4. Thêm visual effects nếu cần

### Thay đổi gameplay:
- **Tốc độ**: Sửa `INIT_BLOCK_SPEED`, `INIT_PLAYER_SPEED`
- **Kích thước**: Sửa `PLAYER_SIZE`, `BLOCK_SIZE`
- **Spawn rate**: Sửa logic trong `updateGame()`
- **Điểm số**: Sửa `scoreMultiplier` logic

### Thêm âm thanh:
1. Thêm file audio vào `public/sounds/`
2. Sử dụng `playSound()` function
3. Hoặc sử dụng HTML5 Audio API cho file âm thanh

### Styling:
- **Colors**: Sửa trong Tailwind classes
- **Fonts**: Thêm vào `globals.css`
- **Animations**: Sử dụng CSS animations hoặc Framer Motion

## 🐛 Troubleshooting

### Lỗi thường gặp:

#### "Module not found":
```bash
# Xóa node_modules và cài lại
rm -rf node_modules package-lock.json
npm install
```

#### "Port 3000 already in use":
```bash
# Sử dụng port khác
npm run dev -- -p 3001
```

#### Canvas không hiển thị:
- Kiểm tra browser console cho errors
- Đảm bảo canvas ref được set đúng
- Kiểm tra CSS không che canvas

#### Game lag/stuttering:
- Giảm số lượng particles
- Tối ưu game loop
- Kiểm tra browser performance

### Performance Tips:
- Sử dụng `requestAnimationFrame` thay vì `setInterval`
- Object pooling cho blocks và particles
- Giới hạn số lượng objects trên màn hình
- Sử dụng `OffscreenCanvas` cho heavy rendering


---

**Chúc bạn chơi game vui vẻ! 🎮**