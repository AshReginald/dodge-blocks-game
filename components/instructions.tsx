"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, ArrowRight, Zap, Shield, Star } from "lucide-react"

interface InstructionsProps {
  onBack: () => void
}

export default function Instructions({ onBack }: InstructionsProps) {
  return (
    <Card className="w-96 bg-gradient-to-br from-blue-600/20 to-purple-600/20 border-white/20 text-white">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">How to Play</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="flex gap-1">
              <ArrowLeft className="h-5 w-5 text-cyan-400" />
              <ArrowRight className="h-5 w-5 text-cyan-400" />
            </div>
            <span>Move left/right with arrow keys or A/D</span>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-4 h-4 bg-red-500 rounded"></div>
            <span>Avoid the falling red blocks</span>
          </div>

          <div className="flex items-center gap-3">
            <Star className="h-5 w-5 text-yellow-400" />
            <span>Collect power-ups for special abilities</span>
          </div>

          <div className="flex items-center gap-3">
            <Shield className="h-5 w-5 text-blue-400" />
            <span>Blue shield gives temporary protection</span>
          </div>

          <div className="flex items-center gap-3">
            <Zap className="h-5 w-5 text-purple-400" />
            <span>Purple speed boost increases movement</span>
          </div>
        </div>

        <div className="bg-white/10 rounded-lg p-3 text-sm">
          <h4 className="font-semibold mb-2">Special Events:</h4>
          <ul className="space-y-1 text-white/80">
            <li>• Big Blocks - Larger falling blocks</li>
            <li>• Fast Blocks - Increased falling speed</li>
            <li>• Mirror Mode - Reversed controls</li>
            <li>• Block Rain - Multiple blocks spawn</li>
            <li>• Ghost Blocks - Some blocks become invisible</li>
          </ul>
        </div>

        <Button onClick={onBack} variant="outline" className="w-full border-white/30 text-white hover:bg-white/10">
          Back to Menu
        </Button>
      </CardContent>
    </Card>
  )
}
