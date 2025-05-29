"use client"

import { useState, useEffect } from "react"
import GameCanvas from "@/components/game-canvas"
import MainMenu from "@/components/main-menu"
import GameOver from "@/components/game-over"
import Instructions from "@/components/instructions"
import { Button } from "@/components/ui/button"
import { Volume2, VolumeX } from "lucide-react"

export type GameState = "menu" | "playing" | "paused" | "gameOver" | "instructions"

export interface GameStats {
  score: number
  highScore: number
  level: number
  blocksDestroyed: number
}

export default function Home() {
  const [gameState, setGameState] = useState<GameState>("menu")
  const [gameStats, setGameStats] = useState<GameStats>({
    score: 0,
    highScore: 0,
    level: 1,
    blocksDestroyed: 0,
  })
  const [soundEnabled, setSoundEnabled] = useState(true)

  useEffect(() => {
    // Load high score from localStorage
    const savedHighScore = localStorage.getItem("dodgeBlocksHighScore")
    if (savedHighScore) {
      setGameStats((prev) => ({ ...prev, highScore: Number.parseInt(savedHighScore) }))
    }
  }, [])

  const startGame = () => {
    setGameState("playing")
    setGameStats((prev) => ({ ...prev, score: 0, level: 1, blocksDestroyed: 0 }))
  }

  const pauseGame = () => {
    setGameState("paused")
  }

  const resumeGame = () => {
    setGameState("playing")
  }

  const endGame = (finalScore: number) => {
    const newHighScore = Math.max(finalScore, gameStats.highScore)
    if (newHighScore > gameStats.highScore) {
      localStorage.setItem("dodgeBlocksHighScore", newHighScore.toString())
    }
    setGameStats((prev) => ({ ...prev, score: finalScore, highScore: newHighScore }))
    setGameState("gameOver")
  }

  const goToMenu = () => {
    setGameState("menu")
  }

  const showInstructions = () => {
    setGameState("instructions")
  }

  const toggleSound = () => {
    setSoundEnabled(!soundEnabled)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="relative">
        {/* Sound Toggle */}
        <Button
          variant="outline"
          size="icon"
          className="absolute top-4 right-4 z-10 bg-white/10 border-white/20 text-white hover:bg-white/20"
          onClick={toggleSound}
        >
          {soundEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
        </Button>

        {/* Game Container */}
        <div className="bg-black/20 backdrop-blur-sm rounded-2xl p-6 shadow-2xl border border-white/10">
          {gameState === "menu" && (
            <MainMenu onStartGame={startGame} onShowInstructions={showInstructions} highScore={gameStats.highScore} />
          )}

          {gameState === "instructions" && <Instructions onBack={goToMenu} />}

          {(gameState === "playing" || gameState === "paused") && (
            <GameCanvas
              gameState={gameState}
              onPause={pauseGame}
              onResume={resumeGame}
              onGameOver={endGame}
              onUpdateStats={setGameStats}
              soundEnabled={soundEnabled}
            />
          )}

          {gameState === "gameOver" && (
            <GameOver score={gameStats.score} highScore={gameStats.highScore} onRestart={startGame} onMenu={goToMenu} />
          )}
        </div>
      </div>
    </div>
  )
}
