"use client"

import { useEffect, useRef, useCallback, useState } from "react"
import type { GameState, GameStats } from "@/app/page"
import { Button } from "@/components/ui/button"
import { Pause, Play } from "lucide-react"

interface GameCanvasProps {
  gameState: GameState
  onPause: () => void
  onResume: () => void
  onGameOver: (score: number) => void
  onUpdateStats: (stats: GameStats) => void
  soundEnabled: boolean
}

interface GameObject {
  x: number
  y: number
  width: number
  height: number
  color: string
  speed?: number
}

interface PowerUp extends GameObject {
  type: "shield" | "speed" | "score"
  collected?: boolean
}

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  life: number
  maxLife: number
  color: string
  size: number
}

export default function GameCanvas({
  gameState,
  onPause,
  onResume,
  onGameOver,
  onUpdateStats,
  soundEnabled,
}: GameCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const gameLoopRef = useRef<number>()
  const keysPressed = useRef<{ [key: string]: boolean }>({})
  const [gameInitialized, setGameInitialized] = useState(false)

  const gameStateRef = useRef<{
    player: GameObject
    blocks: GameObject[]
    powerUps: PowerUp[]
    particles: Particle[]
    score: number
    level: number
    blockSpeed: number
    playerSpeed: number
    blockSize: number
    lastBlockSpawn: number
    lastPowerUpSpawn: number
    activeEvents: { [key: string]: number }
    eventEndTimes: { [key: string]: number }
    warningText: string
    warningTimer: number
    bgColor: string
    scoreMultiplier: number
    shieldActive: boolean
    shieldTimer: number
    speedBoostActive: boolean
    speedBoostTimer: number
    nextEventTime: number
  }>()

  const CANVAS_WIDTH = 400
  const CANVAS_HEIGHT = 600
  const PLAYER_SIZE = 40
  const BLOCK_SIZE = 40
  const INIT_BLOCK_SPEED = 3
  const INIT_PLAYER_SPEED = 6

  const playSound = useCallback(
    (frequency: number, duration: number, type: "sine" | "square" | "triangle" = "sine") => {
      if (!soundEnabled) return

      try {
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
        const oscillator = audioContext.createOscillator()
        const gainNode = audioContext.createGain()

        oscillator.connect(gainNode)
        gainNode.connect(audioContext.destination)

        oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime)
        oscillator.type = type

        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration)

        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + duration)
      } catch (error) {
        // Ignore audio errors
      }
    },
    [soundEnabled],
  )

  const createParticles = useCallback((x: number, y: number, color: string, count = 5) => {
    const particles: Particle[] = []
    for (let i = 0; i < count; i++) {
      particles.push({
        x,
        y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8,
        life: 60,
        maxLife: 60,
        color,
        size: Math.random() * 4 + 2,
      })
    }
    return particles
  }, [])

  const initGame = useCallback(() => {
    gameStateRef.current = {
      player: {
        x: CANVAS_WIDTH / 2 - PLAYER_SIZE / 2,
        y: CANVAS_HEIGHT - PLAYER_SIZE - 10,
        width: PLAYER_SIZE,
        height: PLAYER_SIZE,
        color: "#0080ff",
      },
      blocks: [],
      powerUps: [],
      particles: [],
      score: 0,
      level: 1,
      blockSpeed: INIT_BLOCK_SPEED,
      playerSpeed: INIT_PLAYER_SPEED,
      blockSize: BLOCK_SIZE,
      lastBlockSpawn: 0,
      lastPowerUpSpawn: 0,
      activeEvents: {},
      eventEndTimes: {},
      warningText: "",
      warningTimer: 0,
      bgColor: "#1a1a2e",
      scoreMultiplier: 1,
      shieldActive: false,
      shieldTimer: 0,
      speedBoostActive: false,
      speedBoostTimer: 0,
      nextEventTime: Date.now() + 10000,
    }
    setGameInitialized(true)
  }, [])

  const spawnBlock = useCallback(() => {
    const state = gameStateRef.current!
    const x = Math.random() * (CANVAS_WIDTH - state.blockSize)
    state.blocks.push({
      x,
      y: -state.blockSize,
      width: state.blockSize,
      height: state.blockSize,
      color: "#ff0000",
      speed: state.blockSpeed,
    })
  }, [])

  const spawnPowerUp = useCallback(() => {
    const state = gameStateRef.current!
    const types: PowerUp["type"][] = ["shield", "speed", "score"]
    const type = types[Math.floor(Math.random() * types.length)]
    const colors = { shield: "#4080ff", speed: "#8040ff", score: "#ffff40" }

    state.powerUps.push({
      x: Math.random() * (CANVAS_WIDTH - 30),
      y: -30,
      width: 30,
      height: 30,
      color: colors[type],
      type,
      speed: 2,
    })
  }, [])

  const triggerEvent = useCallback(() => {
    const state = gameStateRef.current!
    const events = [
      "BIG_BLOCKS",
      "FAST_BLOCKS",
      "MIRROR_MODE",
      "BLOCK_RAIN",
      "GHOST_BLOCKS",
      "COLOR_CHANGE",
      "TINY_BLOCKS",
      "SLOW_MOTION",
      "GRAVITY_FLIP",
      "MAGNET_PULL",
      "INVISIBLE_PLAYER",
      "DOUBLE_SCORE",
      "FREEZE_BLOCKS",
      "SPIRAL_BLOCKS",
      "EARTHQUAKE",
      "LASER_BEAM",
      "SHIELD_RAIN",
      "TELEPORT_BLOCKS",
    ]
    const event = events[Math.floor(Math.random() * events.length)]

    state.activeEvents[event] = Date.now()
    state.eventEndTimes[event] = Date.now() + 6000
    state.warningText = event.replace("_", " ")
    state.warningTimer = Date.now()
    state.nextEventTime = Date.now() + Math.random() * 15000 + 8000

    playSound(200, 0.3, "triangle")

    switch (event) {
      case "BIG_BLOCKS":
        state.blockSize = BLOCK_SIZE * 1.8
        break
      case "TINY_BLOCKS":
        state.blockSize = BLOCK_SIZE * 0.6
        break
      case "FAST_BLOCKS":
        state.blockSpeed += 3
        state.scoreMultiplier = 3
        break
      case "SLOW_MOTION":
        state.blockSpeed = Math.max(1, state.blockSpeed * 0.3)
        state.playerSpeed = state.playerSpeed * 0.5
        break
      case "COLOR_CHANGE":
        state.bgColor = `hsl(${Math.random() * 360}, 70%, 15%)`
        break
      case "BLOCK_RAIN":
        for (let i = 0; i < 12; i++) {
          setTimeout(() => spawnBlock(), i * 80)
        }
        break
      case "GRAVITY_FLIP":
        // Blocks will move upward instead
        state.blockSpeed = -Math.abs(state.blockSpeed)
        break
      case "MAGNET_PULL":
        // Blocks will be attracted to player
        break
      case "INVISIBLE_PLAYER":
        // Player becomes semi-transparent
        break
      case "DOUBLE_SCORE":
        state.scoreMultiplier = 4
        break
      case "FREEZE_BLOCKS":
        state.blockSpeed = 0
        break
      case "SPIRAL_BLOCKS":
        // Blocks will move in spiral pattern
        break
      case "EARTHQUAKE":
        // Screen shake effect
        break
      case "LASER_BEAM":
        // Horizontal laser that player must duck under
        break
      case "SHIELD_RAIN":
        // Spawn multiple shield power-ups
        for (let i = 0; i < 3; i++) {
          setTimeout(() => {
            const state = gameStateRef.current!
            state.powerUps.push({
              x: Math.random() * (CANVAS_WIDTH - 30),
              y: -30,
              width: 30,
              height: 30,
              color: "#4080ff",
              type: "shield",
              speed: 2,
            })
          }, i * 500)
        }
        break
      case "TELEPORT_BLOCKS":
        // Blocks randomly teleport
        break
    }
  }, [playSound, spawnBlock])

  const checkCollision = useCallback((rect1: GameObject, rect2: GameObject) => {
    return (
      rect1.x < rect2.x + rect2.width &&
      rect1.x + rect1.width > rect2.x &&
      rect1.y < rect2.y + rect2.height &&
      rect1.y + rect1.height > rect2.y
    )
  }, [])

  const handleInput = useCallback(() => {
    if (!gameStateRef.current) return

    const state = gameStateRef.current
    const speed = state.playerSpeed
    const mirrorMode = state.activeEvents.MIRROR_MODE
    const direction = mirrorMode ? -1 : 1

    if (keysPressed.current["ArrowLeft"] || keysPressed.current["a"] || keysPressed.current["A"]) {
      state.player.x = Math.max(0, state.player.x - speed * direction)
    }
    if (keysPressed.current["ArrowRight"] || keysPressed.current["d"] || keysPressed.current["D"]) {
      state.player.x = Math.min(CANVAS_WIDTH - state.player.width, state.player.x + speed * direction)
    }
  }, [])

  const updateGame = useCallback(() => {
    if (!gameStateRef.current) return

    const state = gameStateRef.current
    const now = Date.now()

    // Handle input
    handleInput()

    // Handle active events
    Object.keys(state.eventEndTimes).forEach((event) => {
      if (now > state.eventEndTimes[event]) {
        delete state.activeEvents[event]
        delete state.eventEndTimes[event]

        switch (event) {
          case "BIG_BLOCKS":
          case "TINY_BLOCKS":
            state.blockSize = BLOCK_SIZE
            break
          case "FAST_BLOCKS":
            state.blockSpeed = INIT_BLOCK_SPEED + Math.floor(state.score / 100)
            state.scoreMultiplier = 1
            break
          case "SLOW_MOTION":
            state.blockSpeed = INIT_BLOCK_SPEED + Math.floor(state.score / 100)
            state.playerSpeed = state.speedBoostActive ? INIT_PLAYER_SPEED * 1.5 : INIT_PLAYER_SPEED
            break
          case "COLOR_CHANGE":
            state.bgColor = "#1a1a2e"
            break
          case "GRAVITY_FLIP":
            state.blockSpeed = Math.abs(state.blockSpeed)
            break
          case "DOUBLE_SCORE":
            state.scoreMultiplier = 1
            break
          case "FREEZE_BLOCKS":
            state.blockSpeed = INIT_BLOCK_SPEED + Math.floor(state.score / 100)
            break
        }

        state.score += 15
        playSound(400, 0.2)
      }
    })

    // Handle power-up timers
    if (state.shieldActive && now > state.shieldTimer) {
      state.shieldActive = false
    }
    if (state.speedBoostActive && now > state.speedBoostTimer) {
      state.speedBoostActive = false
      state.playerSpeed = INIT_PLAYER_SPEED
    }

    // Spawn blocks
    if (now - state.lastBlockSpawn > Math.max(1000 - state.level * 50, 300)) {
      spawnBlock()
      state.lastBlockSpawn = now
    }

    // Spawn power-ups
    if (now - state.lastPowerUpSpawn > 8000 + Math.random() * 7000) {
      spawnPowerUp()
      state.lastPowerUpSpawn = now
    }

    // Trigger events
    if (state.score >= 50 && now > state.nextEventTime && Object.keys(state.activeEvents).length === 0) {
      triggerEvent()
    }

    // Update blocks
    state.blocks = state.blocks.filter((block, index) => {
      let moveX = 0
      let moveY = block.speed || state.blockSpeed

      // Special event behaviors
      if (state.activeEvents.SPIRAL_BLOCKS) {
        const time = Date.now() * 0.005
        moveX = Math.sin(time + index) * 2
      }

      if (state.activeEvents.MAGNET_PULL) {
        const playerCenterX = state.player.x + state.player.width / 2
        const blockCenterX = block.x + block.width / 2
        const attraction = (playerCenterX - blockCenterX) * 0.1
        moveX += attraction
      }

      if (state.activeEvents.TELEPORT_BLOCKS && Math.random() < 0.01) {
        block.x = Math.random() * (CANVAS_WIDTH - block.width)
      }

      if (state.activeEvents.GRAVITY_FLIP) {
        moveY = -Math.abs(moveY)
        if (block.y < -block.height) {
          state.score += state.scoreMultiplier
          return false
        }
      }

      block.x += moveX
      block.y += moveY

      // Keep blocks in bounds
      block.x = Math.max(0, Math.min(CANVAS_WIDTH - block.width, block.x))

      if (!state.activeEvents.GRAVITY_FLIP && block.y > CANVAS_HEIGHT) {
        state.score += state.scoreMultiplier
        return false
      }

      if (checkCollision(state.player, block) && !state.shieldActive) {
        playSound(150, 0.5, "square")
        onGameOver(state.score)
        return false
      }

      return true
    })

    // Update power-ups
    state.powerUps = state.powerUps.filter((powerUp) => {
      powerUp.y += powerUp.speed || 2

      if (powerUp.y > CANVAS_HEIGHT) return false

      if (checkCollision(state.player, powerUp) && !powerUp.collected) {
        powerUp.collected = true
        playSound(600, 0.3)

        state.particles.push(...createParticles(powerUp.x + 15, powerUp.y + 15, powerUp.color))

        switch (powerUp.type) {
          case "shield":
            state.shieldActive = true
            state.shieldTimer = now + 5000
            break
          case "speed":
            state.speedBoostActive = true
            state.speedBoostTimer = now + 5000
            state.playerSpeed = INIT_PLAYER_SPEED * 1.5
            break
          case "score":
            state.score += 50
            break
        }
        return false
      }

      return true
    })

    // Update particles
    state.particles = state.particles.filter((particle) => {
      particle.x += particle.vx
      particle.y += particle.vy
      particle.life--
      particle.vx *= 0.98
      particle.vy *= 0.98
      return particle.life > 0
    })

    // Update level
    const newLevel = Math.floor(state.score / 100) + 1
    if (newLevel > state.level) {
      state.level = newLevel
      state.blockSpeed = INIT_BLOCK_SPEED + state.level * 0.5
      playSound(800, 0.4)
    }

    onUpdateStats({
      score: state.score,
      highScore: 0,
      level: state.level,
      blocksDestroyed: state.score,
    })
  }, [
    checkCollision,
    createParticles,
    handleInput,
    onGameOver,
    onUpdateStats,
    playSound,
    spawnBlock,
    spawnPowerUp,
    triggerEvent,
  ])

  const render = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas || !gameStateRef.current) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const state = gameStateRef.current

    // Clear canvas with background
    ctx.fillStyle = state.bgColor
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

    // Draw particles
    state.particles.forEach((particle) => {
      const alpha = particle.life / particle.maxLife
      ctx.globalAlpha = alpha
      ctx.fillStyle = particle.color
      ctx.beginPath()
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
      ctx.fill()
    })
    ctx.globalAlpha = 1

    // Add earthquake effect
    let shakeX = 0,
      shakeY = 0
    if (state.activeEvents.EARTHQUAKE) {
      shakeX = (Math.random() - 0.5) * 10
      shakeY = (Math.random() - 0.5) * 10
      ctx.translate(shakeX, shakeY)
    }

    // Draw player with special effects
    if (state.shieldActive) {
      ctx.strokeStyle = "#4080ff"
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.arc(
        state.player.x + state.player.width / 2,
        state.player.y + state.player.height / 2,
        state.player.width / 2 + 5,
        0,
        Math.PI * 2,
      )
      ctx.stroke()
    }

    // Invisible player effect
    if (state.activeEvents.INVISIBLE_PLAYER) {
      ctx.globalAlpha = 0.3
    }

    ctx.fillStyle = state.speedBoostActive ? "#ff8040" : state.player.color
    ctx.fillRect(state.player.x, state.player.y, state.player.width, state.player.height)
    ctx.globalAlpha = 1

    // Draw laser beam
    if (state.activeEvents.LASER_BEAM) {
      const laserY = CANVAS_HEIGHT * 0.7
      ctx.fillStyle = "#ff0040"
      ctx.fillRect(0, laserY - 5, CANVAS_WIDTH, 10)

      // Check laser collision
      if (state.player.y + state.player.height > laserY - 5 && state.player.y < laserY + 5 && !state.shieldActive) {
        playSound(150, 0.5, "square")
        onGameOver(state.score)
      }
    }

    // Reset earthquake transform
    if (state.activeEvents.EARTHQUAKE) {
      ctx.translate(-shakeX, -shakeY)
    }

    // Draw blocks
    state.blocks.forEach((block) => {
      if (state.activeEvents.GHOST_BLOCKS && Math.random() < 0.3) {
        ctx.globalAlpha = 0.3
      }
      if (state.activeEvents.HIDDEN_BLOCKS && block.y > CANVAS_HEIGHT / 2) {
        return
      }

      ctx.fillStyle = block.color
      ctx.fillRect(block.x, block.y, block.width, block.height)
      ctx.globalAlpha = 1
    })

    // Draw power-ups
    state.powerUps.forEach((powerUp) => {
      ctx.fillStyle = powerUp.color
      ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height)

      // Draw power-up symbol
      ctx.fillStyle = "#ffffff"
      ctx.font = "16px Arial"
      ctx.textAlign = "center"
      const symbol = powerUp.type === "shield" ? "🛡️" : powerUp.type === "speed" ? "⚡" : "⭐"
      ctx.fillText(symbol, powerUp.x + 15, powerUp.y + 20)
    })

    // Draw UI
    ctx.fillStyle = "#ffffff"
    ctx.font = "20px Arial"
    ctx.textAlign = "left"
    ctx.fillText(`Score: ${state.score}`, 10, 30)
    ctx.fillText(`Level: ${state.level}`, 10, 55)

    // Draw active events
    let effectY = 80
    Object.keys(state.activeEvents).forEach((event) => {
      ctx.fillStyle = "#ffff40"
      ctx.font = "14px Arial"
      ctx.textAlign = "left"
      ctx.fillText(`⚡ ${event.replace("_", " ")}`, 10, effectY)
      effectY += 20
    })

    if (state.shieldActive) {
      ctx.fillStyle = "#4080ff"
      ctx.fillText("🛡️ Shield Active", 10, effectY)
      effectY += 20
    }
    if (state.speedBoostActive) {
      ctx.fillStyle = "#8040ff"
      ctx.fillText("⚡ Speed Boost", 10, effectY)
      effectY += 20
    }

    // Draw warning text
    if (state.warningText && Date.now() - state.warningTimer < 2000) {
      ctx.fillStyle = "#ff4040"
      ctx.font = "bold 24px Arial"
      ctx.textAlign = "center"
      ctx.fillText(`⚠️ ${state.warningText}`, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    }

    // Draw pause overlay
    if (gameState === "paused") {
      ctx.fillStyle = "rgba(0, 0, 0, 0.7)"
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
      ctx.fillStyle = "#ffffff"
      ctx.font = "bold 36px Arial"
      ctx.textAlign = "center"
      ctx.fillText("PAUSED", CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    }
  }, [gameState, onGameOver])

  const gameLoop = useCallback(() => {
    if (gameState === "playing" && gameInitialized) {
      updateGame()
    }
    render()
    gameLoopRef.current = requestAnimationFrame(gameLoop)
  }, [gameState, gameInitialized, updateGame, render])

  // Initialize game when component mounts
  useEffect(() => {
    initGame()
  }, [initGame])

  // Start game loop when game is initialized
  useEffect(() => {
    if (gameInitialized) {
      gameLoopRef.current = requestAnimationFrame(gameLoop)
    }

    return () => {
      if (gameLoopRef.current) {
        cancelAnimationFrame(gameLoopRef.current)
      }
    }
  }, [gameInitialized, gameLoop])

  // Handle keyboard input
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      keysPressed.current[e.key] = true

      if (e.key === " ") {
        e.preventDefault()
        if (gameState === "playing") {
          onPause()
        } else if (gameState === "paused") {
          onResume()
        }
      }
    }

    const handleKeyUp = (e: KeyboardEvent) => {
      keysPressed.current[e.key] = false
    }

    window.addEventListener("keydown", handleKeyDown)
    window.addEventListener("keyup", handleKeyUp)

    return () => {
      window.removeEventListener("keydown", handleKeyDown)
      window.removeEventListener("keyup", handleKeyUp)
    }
  }, [gameState, onPause, onResume])

  return (
    <div className="relative">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-white">Dodge Blocks</h2>
        <Button
          onClick={gameState === "playing" ? onPause : onResume}
          variant="outline"
          size="sm"
          className="border-white/30 text-white hover:bg-white/10"
        >
          {gameState === "playing" ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
        </Button>
      </div>

      <canvas
        ref={canvasRef}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        className="border-2 border-white/20 rounded-lg bg-gray-900"
      />

      <div className="mt-4 text-center text-white/80 text-sm">Use ← → or A/D to move • Space to pause</div>
    </div>
  )
}
