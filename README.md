# Very's Chess Interpreter
convert an image of a chess.com game(in expanded mode) to FEN format using **computer vision**.

## Failed attempt #1
;( 
### Input
![oof](https://i.imgur.com/oulKJ5U.png)
### Output
![oof](https://cdn.discordapp.com/attachments/558675537879367681/558786403236839434/unknown.png)
###
Converted input into grayscale, then *independently* cycled through each template. This brought up many false flags and was very inaccurate. 

#### Runtime
Around 5 seconds.
## Attempt #2: SUCCESS!!
:D
### Input
![yeet](https://cdn.discordapp.com/attachments/558675537879367681/559088859107819634/unknown.png)
### Processed Image
![yeet](https://media.discordapp.net/attachments/558675537879367681/559088923624603658/unknown.png)
### Output
`8/4q3/8/4KP2/7p/7P/2k5/8 w - - 0 1`
### Explanation
First: Converted input into grayscale, then converted grayscale into binary. Found where the chessboard was by getting the largest contour, then split the chessboard into 64 squares based on the positions of the contour. Used template matching to find the piece in each square, and converted this to FEN format.
#### Runtime
Around 0.6 seconds.
