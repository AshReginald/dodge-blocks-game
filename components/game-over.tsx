"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RotateCcw, Home, Trophy, Target } from "lucide-react"

interface GameOverProps {
  score: number
  highScore: number
  onRestart: () => void
  onMenu: () => void
}

export default function GameOver({ score, highScore, onRestart, onMenu }: GameOverProps) {
  const isNewHighScore = score === highScore && score > 0

  return (
    <Card className="w-96 bg-gradient-to-br from-red-600/20 to-orange-600/20 border-white/20 text-white">
      <CardHeader className="text-center">
        <CardTitle className="text-3xl font-bold text-red-400">Game Over</CardTitle>
        {isNewHighScore && <div className="text-yellow-400 font-semibold animate-pulse">🎉 New High Score! 🎉</div>}
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-2">
            <Target className="h-6 w-6 text-white" />
            <span className="text-lg">Final Score</span>
          </div>
          <div className="text-4xl font-bold text-white">{score.toLocaleString()}</div>

          <div className="flex items-center justify-center gap-2 text-yellow-400">
            <Trophy className="h-5 w-5" />
            <span>Best: {highScore.toLocaleString()}</span>
          </div>
        </div>

        <div className="space-y-3">
          <Button
            onClick={onRestart}
            className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold"
            size="lg"
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            Play Again
          </Button>

          <Button
            onClick={onMenu}
            variant="outline"
            className="w-full border-white/30 text-white hover:bg-white/10"
            size="lg"
          >
            <Home className="mr-2 h-4 w-4" />
            Main Menu
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
