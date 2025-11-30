# Chess Opening Memorization Trainer

An interactive Streamlit app designed to help you **actively memorize** your personalized chess opening repertoire through quizzes, spaced repetition, and random testing.

## Your Repertoire

### As White:
- **Catalan Opening** (Closed & Open variations) - Your main weapon
- **Italian Game** (Giuoco Piano) - Backup for tactical games

### As Black vs 1.e4:
- **Caro-Kann Defense** (Classical & Advance variations)

### As Black vs 1.d4:
- **Queen's Gambit Declined** (Orthodox) - Solid main line
- **King's Indian Defense** - Attacking option

## How to Use

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run chess_opening_app.py
   ```

3. **Choose your training mode:**
   - **📖 Study Mode**: View moves step-by-step with auto-play
   - **🎯 Quiz Mode**: Guess the next move and get instant feedback
   - **🎲 Random Test**: Jump to random positions to test your memory

4. **Track your progress:**
   - Mark openings as mastered with the checkbox button
   - See which openings need review (🔔 bell icon)
   - Track your quiz accuracy scores

## Features

### Active Learning Tools
- 🎯 **Quiz Mode** - Test yourself on every move with instant feedback
- 🎲 **Random Position Testing** - Jump to any position and prove you know it
- ✅ **Progress Tracking** - Simple checkmarks to track mastered openings
- 🔔 **Spaced Repetition** - Automatic reminders for when to review each opening

### Study Features
- 📖 **Study Mode** - Traditional step-by-step navigation with auto-play
- ♟️ **Interactive Board** - Visual chess board for all positions
- 💡 **Key Ideas** - Important concepts highlighted for each move
- 📋 **Strategic Plans** - Overall game plan for each opening

### Spaced Repetition Schedule
The app automatically tracks when you should review each opening:
- First review: 1 day after initial study
- Second review: 3 days later
- Third review: 7 days later
- Fourth review: 14 days later
- Fifth+ review: 30 days later

## How to Memorize Effectively

1. **Start with Study Mode** - Learn the moves and understand the ideas
2. **Switch to Quiz Mode** - Test yourself immediately after studying
3. **Use Random Testing** - Once confident, test random positions
4. **Mark as Mastered** - Only when you can complete the opening without errors
5. **Review Regularly** - Check for 🔔 bell icons showing openings due for review

## 8-Week Memorization Plan

| Week | Focus | Study Method | Goal |
|------|-------|--------------|------|
| 1-2  | Catalan as White | Study → Quiz → Random Test daily | 90%+ quiz accuracy |
| 3-4  | Italian Game as White | Study → Quiz → Random Test daily | 90%+ quiz accuracy |
| 5-6  | Caro-Kann as Black | Study → Quiz → Random Test daily | 90%+ quiz accuracy |
| 7-8  | QGD & KID as Black | Study → Quiz → Random Test daily | 90%+ quiz accuracy |

### Daily Routine (15-20 minutes)
1. Check for 🔔 review notifications - review those first
2. Study new opening in Study Mode (5 min)
3. Quiz yourself on the same opening (5 min)
4. Random position testing (5 min)
5. Mark as mastered when you hit 90%+ accuracy

## Progress Tracking

Your progress is automatically saved to `~/.chess_opening_progress.json`. This includes:
- Which openings you've marked as mastered
- When you last reviewed each opening
- Number of times you've reviewed each opening

Good luck mastering your repertoire!
