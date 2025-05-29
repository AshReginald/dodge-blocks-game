"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Play, HelpCircle, Trophy } from "lucide-react"

interface MainMenuProps {
  onStartGame: () => void
  onShowInstructions: () => void
  highScore: number
}

export default function MainMenu({ onStartGame, onShowInstructions, highScore }: MainMenuProps) {
  return (
    <Card className="w-96 bg-gradient-to-br from-blue-600/20 to-purple-600/20 border-white/20 text-white">
      <CardHeader className="text-center">
        <CardTitle className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
          🚧 Dodge Blocks
        </CardTitle>
        <p className="text-white/80 text-lg">Survive the falling chaos!</p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 text-yellow-400 mb-2">
            <Trophy className="h-5 w-5" />
            <span className="text-lg font-semibold">High Score</span>
          </div>
          <div className="text-3xl font-bold text-white">{highScore.toLocaleString()}</div>
        </div>

        <div className="space-y-3">
          <Button
            onClick={onStartGame}
            className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 text-lg"
            size="lg"
          >
            <Play className="mr-2 h-5 w-5" />
            Start Game
          </Button>

          <Button
            onClick={onShowInstructions}
            variant="outline"
            className="w-full border-white/30 text-white hover:bg-white/10"
            size="lg"
          >
            <HelpCircle className="mr-2 h-5 w-5" />
            How to Play
          </Button>
        </div>

        <div className="text-center text-white/60 text-sm">Use ← → arrow keys or A/D to move</div>
      </CardContent>
    </Card>
  )
}
