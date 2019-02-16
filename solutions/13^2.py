import sys
import re
import operator as op
input=r"""             /-------------------------------------------\                                                                                            
             |                             /-------------+------------------------------------------\                                                 
             |                             |         /---+------------------------------------------+-\                                               
      /------+-----\  /--------------------+---------+---+------------------------------------------+-+-----------------------\                       
 /----+------+-----+--+--------------------+----\    |   |                                  /-------+-+-----------------------+---\                   
 |    |      |     |  |           /--------+----+----+---+----------------------------------+------\| |                       |   |                   
 |    |      |     |  |           |        |/---+----+---+----------------------------------+------++-+-\                     |   |                   
 |    |  /---+-----+--+-----------+--------++---+----+---+-----------------------\          |      || | |                     |   |                   
/+----+--+---+-----+--+-----------+--------++---+----+---+---\      /------------+----------+------++-+-+-----------\         |   |                   
||    |  |   |     |  |           |        ||   |    |   |   |      |            |          |      || | |  /--------+---------+---+-----------------\ 
||    |  |   \-----+--+-----------+--------++---+----+---/   |/-----+------------+----\     |      || | |  |        |         |   |                 | 
||    |  |         |  |           | /------++\  |    |    /--++-----+\           |    |     |      || | |  |        |         |   |                 | 
||    |  |         |  |           | |      |||  |    |    |  ||/----++-----------+----+-----+------++-+-+--+----\   |         |   |                 | 
||    |  |         |  |           | |      ||| /+----+----+--+++----++-----------+<---+-----+------++-+-+--+----+---+---------+---+----------\      | 
||    |  |         |  |           | |      ||| ||    |    |  |^|    ||           |    |/----+------++-+-+--+----+---+---------+---+\         |      | 
||    |  |         |  |           | |      ||| ||    |    |  |||    ||           |    ||    |      || | | /+----+---+---------+\  ||         |      | 
|| /--+--+---------+--+-----------+-+------+++-++----+----+--+++----++-----\     |    ||    |      || | | ||    |   |         ||  ||         |      | 
|| |  |  |         |  |           | |      ||| ||    |    |  |||    ||     |     |    ||    |      || | | ||    |   |         ||  ||         |      | 
|| |  |  |         |  |           | |      |||/++----+----+--+++----++-----+-----+----++----+------++-+-+-++----+---+-------\ ||  ||         |      | 
|| |  |  |         |  |           |/+------++++++----+-\  |  |||    ||     |     |    ||    |      || | | ||    |   |       | ||  ||         |      | 
|| |/-+--+---------+--+-----------+++------++++++----+-+--+--+++----++----\|     |    ||    |      || | | ||    |   |       | ||  ||         |      | 
|| || |  |         |  |           |||      ||||||    | | /+--+++----++----++-----+----++----+------++-+-+-++----+--\|       | ||  ||         |      | 
|| || |  |         |  |           |||      ||||||    | | ||  |||    ||    ||     |    ||    |      || | | ||    |  ||       | ||  ||         |      | 
|| || |  |       /-+--+--------\  ||\------++/|||    | | ||  |||    ||    ||     |    ||    |      || | | ||    |  ||       | ||  ||         |      | 
|| || |  |   /---+-+--+--------+--++-------++-+++----+-+-++--+++----++----++-----+-\  ||    |      || | | ||    |  ||       | ||  ||         |      | 
|\-++-+--+---+---+-+--+--------+--++-------++-++/    | | |\--+++----+/    ||     | |  ||    |      || | | ||    |  ||       | ||  ||         |      | 
|  || |  |   |   | |  |  /-----+--++-\     || ||     | | |   |||    |     ||     | |  ||    |      || | | |^    |  ||       | ||  ||         |      | 
|  || |  |   |   | |  |  |     |  || |     || ||     \-+-+---+++----+-----++-----+-+--++----+------++-/ | ||    |  ||       | ||  ||         |      | 
|  || |  |   |   | |  |  |     |  || |/----++-++-->----+-+---+++----+-----++-----+-+--++----+------++---+-++----+--++------\| ||  ||         |      | 
|  || |  |/--+---+-+--+--+-----+--++-++----++-++-------+-+---+++\  /+-----++-----+-+--++--\ |      ||   | |\----+--++------++-++--++---------+------/ 
|  || |  ||  |   | |  |  |     |  || ||    || ||       | |   ||||  ||     ||     | |  ||  | |      ||   | \-----+--++------++-+/  ||         |        
|  || |  ||  |   | |  |  |   /-+--++-++----++-++-------+-+---++++--++-----++-----+-+--++--+-+------++---+-------+--++------++-+---++\        |        
|  || |  ||  |   | |  |  |   | |  || ||    || ||       | |   ||||  ||/----++--\  | |  ||  | |      ||  /+-------+--++\     || |   |||        |        
|  |\-+--++--+---+-+--+--+---+-+--++-++----++-++-------+-+---++++--+++----/|  |  | |  ||  | |      ||/-++-------+--+++-----++-+---+++-------\|        
|  |  |  ||  |   | |  |  |   |/+--++-++----++-++-------+-+---++++--+++-----+--+--+-+--++--+-+------+++-++----\  |  ||| /---++-+---+++-------++\       
|  |  |  ||  |   | |  |  | /-+++--++-++----++-++-------+-+---++++--+++-----+--+--+-+--++--+-+------+++-++----+--+--+++-+---++-+---+++-\     |||       
|  |  |  ||  |   \-+--+--+-+-++/  || ||    || ||       | |   |||| /+++-----+--+--+-+--++--+-+------+++-++----+--+--+++-+---++-+---+++-+-----+++------\
|  |  |  ||/-+-----+--+--+-+-++--\|| ||    || ||    /--+-+---++++-++++-----+--+--+-+--++--+-+------+++-++----+--+--+++-+-\ || |   ||| |     |||      |
|  |  |  ||| |     |  |  | | ||  ||| ||    || ||    |  | |   |||| ||||    /+--+--+-+--++--+-+------+++-++----+--+--+++-+-+-++-+---+++-+-----+++---\  |
|  |  |  ||| |/----+--+--+-+-++--+++-++----++-++----+--+-+---++++-++++----++--+--+-+-\||  | |      ||| ||    |  |  ||| | | || |   ||| |  /--+++---+-\|
|  |  |  ||| ||    |  |  | | ||  ||| || /--++-++----+--+-+---++++-++++----++--+--+-+-+++--+-+------+++-++----+\ |  ||| | | || |   ||| |  |  |||   | ||
|  |  \--+++-++----/  |  | | ||  ||| || |  || ||    |  | |   |||| |\++----++--+--+-+-+++--/ |      ||| ||    || |  ||| | | || |   ||| |  |  |||   | ||
|  |     ||| ||       |  \-+-++--+++-/|/+--++-++----+--+-+---++++-+-++----++--+--+-+-+++----+------+++-++----++-+--+++-+-+-++-+---+++-+--+--+++-\ | ||
|  |     ||| ||  /----+----+-++--+++--+++--++-++----+\ | |   |||| | ||    ||  |  | | |||    |      ||\-++----++-+--+++-+-+-++-+---+++-+--+--/|| | | ||
|  |     ||| ||  |    |    | ||  ||\--+++--++-++----++-/ \---++++-+-++----++--+--+-+-+++----+------++--++----++-+--/|| | | || |   ||| |  |   || | | ||
|  |     ||| || /+----+----+-++--++---+++--++-++----++-\     |||| | ||    || /+--+-+-+++----+------++--++----++-+---++-+-+-++-+---+++-+\ |   || | | ||
|  |     ||| || ||    |    | ||  ||   |||  || ||    || |     |||| | ||    || ||  | | |||    |      ||  ||    || |   || | | || |   ||| || |   || | | ||
\--+-----+++-++-++----+----+-++--++---+++--++-++----++-+-----/||| | ||    || ||  | | ||\----+------++--++----++-+---++-+-+-++-+---+/| || |   || | | ||
   |     ||| || ||    |    | ||  ||   |||  || ||    || |      \++-+-++----++-++--+-+-+/     |      ||/-++----++\|   || | | |v |   | | || |   || | | ||
   |     ||| || ||    |    |/++--++---+++--++-++----++-+-------++-+-++----++-++-\| | |      \------+++-++----++++---++-+-+-++-+---/ | || |   || | | ||
   |     ||| || ||    |    ||||  ||  /+++--++-++----++-+-------++-+-++----++-++-++-+-+--\          |||/++<---++++---++-+-+-++-+-----+-++-+---++-+-+\||
   |     ||| || ||    |    ||||  ||/-++++--++-++----++-+-------++-+-++----++-++-++-+-+--+----------++++++----++++\  || | | || |     | || |   || | ||||
   |     ||| || ||    |    ||||  ||| ||||  || ||    || |       || | ||    || || || | |  |          ||||||/---+++++--++-+-+-++-+----\| || |   || | ||||
   |     ||| || ||    |    ||||  ||| ||||  ||/++----++-+-------++-+\||    || || || | |  |          |||||||   |||||  || | | || |    || || \---++-+-++/|
   |     ||| || ||    |    ||||  ||| ||||  |||||    ||/+-------++-++++----++-++-++-+-+--+----------+++++++---+++++--++-+-+-++-+----++-++-----++-+-++\|
   |     ||| || ||    |    ||||  ||| ||||  |||||    ||||  /----++-++++----++-++-++-+-+--+----------+++++++---+++++--++-+-+-++-+----++-++-----++-+\||||
   |     |\+-++-++----+----++++--+++-++++--+++++----++++--+----+/ ||||    || || || | |  |       /--+++++++---+++++--++-+-+-++-+-\  || ||     || ||||||
   |  /--+-+-++-++----+----++++--+++-++++--+++++----++++--+----+--++++----++-++-++-+\|  |       |  |||||||   |||||  || | | || | |  || ||     || ||||||
   |  |  | | || || /--+----++++--+++-++++--+++++-\  ||||  |    |  ||||    \+-++-++-+++--+-------+--+++++++---+++++--++-+-+-++-+-+--++-++-----++-++/|||
   |  |/-+-+-++-++-+--+----++++--+++-++++--+++++-+--++++--+----+\ ||\+-----+-++-++-+++--+-------+--+++++++---+++++--/| | | || | |  || ||     || || |||
   |  || | | || || |  |    |\++--+++-++++--+++++-+--++++--+----++-++-+-----+-++-/| |||  |       |  |||||||   |||||   | | | || | |  || ||     || || |||
   |  || | | || ||/+--+----+-++--+++-++++--+++++-+--++++--+----++-++-+-----+-++--+-+++--+-------+--+++++++---+++++\  | | | || | |  ||/++-----++-++\|||
   |  || | | || ||||  |    | ||  ||| ||||  ||||| |  ||||  |    || || |   /-+-++--+-+++--+-------+--+++++++--\||||||  | | | || | |  |||||     || ||||||
   |  || | | || ||||  |    | ||  ||| ||||  ||||\-+--++++--+----++-++-+---+-+-++--+-+++--+-------+--+++++++--+++++++--+-+-+-++-+-+--+++++-----/| ||||||
   |  || | | \+-++++--+----+-++--+++-++++--++++--+--++++--+----++-++-+---+-+-++--+-/||  |       |  |||||||  |||||||  | | | || | |  |||||      | ||||||
   |  || | |  | ||||  | /--+-++--+++-++++--++++--+--++++--+----++-++-+---+-+-++--+--++--+-------+--+++++++--+++++++--+-+-+\|| | |  |||||      | ||||||
   |  ^| | |  | ||||  | |  | ||  ||| ||||  ||||  |  ||||  |    || || |   | | ||  |  ||  |       |  |||||||  |||||||  | | |||| | |  |||||      | ||||||
   | /++-+-+--+-++++--+-+--+-++--+++-++++--++++--+--++++--+----++-++-+---+-+-++--+--++--+------\|  |||||||  |||||||  | | |||| | |  |||||      | ||||||
   | ||| | |  | ||||  | |  | ||  ||| ||||  ||||  |  ||||  |    || || |   | | ||  |  ||  |      ||  |||||||  |||||||  | | |||| | |  |||||      | ||v|||
   | ||| | |  | ||||  | |  | ||  ||| ||||  ||||  |  ||||  |    || || |   | |/++--+--++--+---\  ||  |||||||  |||||||  | | |||| | |  |||||      | ||||||
   | ||| | |  |/++++--+-+--+-++--+++-++++--++++--+--++++--+----++-++-+---+-++++--+--++--+---+--++--+++++++-\|||||||  | | |||| | |  |||||      | ||||||
   | ||| | |  ||||||  | |  | |\--+++-++++--++++--+--++++--+----++-++-+---+-++++--+--++--+---+--++--+++++++-++/|||||  | | |||| | |  |||||      | ||||||
   | ||| | |  ||||||  | |  | |   ||| ||||  ||||  |  ||||  |    || || |   | ||||  |  ||  |   |  ||  ||||||| || |||||  | | |||| | |  |||||      | ||||||
   | ||| | |  ||||||  | |  | |   ||\-++++--++++--+--++++--+----++-++-+---+-++++--+--++--+---+--++--+++++++-++-+++/|  | | |||| | |  |||||      | ||||||
   | ||| | |  ||||||  | |  | |   ||  ||||  ||||/-+--++++--+----++-++-+--\| ||||  |  ||  |   |  ||  ||||||| || ||| |  | | |||| | |  |||||      | ||||||
   | ||| | |  ||||||  | |  | |   ||  ||||  ||||| |  ||||  |    || || |  || ||||  |  ||  |   |  ||  ||||||| || ||| |  | | |||| | |  |||||      | ||||||
   | |\+-+-+--++++++--+-+--+-+---++--++++--+++++-+--++++--+----++-++-+--++-++++--+--/|  |   |  ||  ||||||| || ||| |  | | |||| | |  |||||      | ||||||
   |/+-+-+-+--++++++--+-+--+-+---++--++++--+++++-+-\||||  |    ||/++-+--++-++++--+---+--+---+--++--+++++++-++\||| |  |/+-++++-+-+-\|||||      | ||||||
   ||| | | |  ||||||  | |  | |   ||  ||||  ||\++-+-+++++--+----++++/ |  || ||||  |   |  |   |  ||  ||||||| |||||| |  ||| |||| | | ||||||      | ||||||
   ||| | | |  ||||||  | |  | | /-++--++++-\\+-++-+-+++++--+----++++--+--++-++++--+---+--+---+--++--+/||||| |||||| |  ||| |||| | | ||||||      | ||||||
   ||| | | |  ||||||  | |  | | | ||  |||| | | || | |||||  |    ||||  |  || ||||  |   |  |   |  |\--+-+++++-++++++-+--+++-++++-+-/ ||||||      | ||||||
 /-+++-+-+-+--++++++--+-+--+-+-+-++--++++-+-+-++-+-+++++--+----++++--+--++-++++-\|   |  |   |  |   | ||\++-++++++-+--/|| |||| |   ||||||      | ||||||
 | ||| | | |  ||||||  | |  | | | ||  |||| | | || | |||||/-+----++++--+--++-++++-++---+--+\  |  |   | |\-++-++++++-+---++-++++-+---++++++------+-+++/||
 | ||| | | |  ||||||  | |  | | | ||  |||| | \-++-+-++++++-+----++++--+--++-++++-++---+--++--+--+---+-+--/| |||||| |   || |||| |   ||||||      | ||| ||
 | ||| | | |  ||||||  | |  | | | |\--++++-+---++-+-++++++-+----++++--+--++-++++-++---+--++--+--+---/ |   | |||||| |   || |||| |   ||||||      | ||| ||
 | ||| | | |  ||\+++--+-+--+-+-+-+---++++-+---++-+-++++/| |    ||||  |  || |||| ||   |  ||  |  |     |/--+-++++++-+---++-++++\|   ||||||      | ||| ||
 | ||| | \-+--++-+++--+-+--+-+-+-+---++++-+---++-+-++++-+-+----++++--+--++-++++-+/   |  ||  |  |     ||  | |||||| |   || ||||||   ||||||      | ||| ||
 | |||/+---+--++-+++\ | |  | | | |   |||| |   || | |||| | |    ||||  |  || |||| |    |  ||  |  |     ||  | |||||| |   \+-++++++---/|||||      | ||| ||
 | |||||  /+--++-++++-+-+--+-+-+-+---++++-+---++-+-++++-+-+----++++--+--++-++++-+----+--++\ |  |     ||  | |||||| |    \-++++++----+++++------/ ||| ||
 | |||||  ||  || |||| | \--+-+-+-+---++++-+---++-+-++++-+-+----++++--+--++-++++-+----+--+++-+--+-----++--+-++++++-+------+/||||    |||||        ||| ||
/+-+++++--++--++-++++-+----+-+-+-+---++++\|   || | |||| | |    ||||  |  || |||| |    | /+++-+--+-----++--+-++++++-+------+-++++----+++++-----\  ||| ||
|| |\+++--++--++-++++-+----+-+-+-+---++++++---++-+-/||| | |    ||||  |  || ||\+-+----+-++++-+--+-----++--+-++++++-+------+-++++----++++/     |  ||| ||
|| | |||  ||  || |||| |    | | | |   ||||||   || |  ||| \-+----++++--+--++-++-+-+----+-++/| |  |     ||  | |||||| |      | ||||    ||||      |  ||| ||
|| | |||  ||  || |||| |    | | | |   ||||||   || |  |||   |    ||\+--+--++-++-+-+----+-++-+-+--+-----++--+-++/||| |      | ||||    ||\+------+--++/ ||
|| | |||  ||/-++-++++-+----+-+-+-+---++++++---++-+--+++---+----++-+--+--++-++-+-+----+-++-+-+--+--\  ||  |/++-+++-+------+-++++----++-+------+\ ||  ||
|| | |||  ||| || |||| |    | | | |   ||||||   || |  |||   |    || |  |  || || | | /--+-++-+-+--+--+--++--++++-+++-+------+-++++--\ || |      || ||  ||
|| | |||  ||| || |||| |    |/+-+-+---++++++---++-+--+++---+----++-+<-+--++-++-+-+-+--+-++-+-+--+--+--++--++++-+++\|      |/++++--+-++-+-\    || ||  ||
|\-+-+++--+++-++-++++-+----+++-+-+---++++++---++-+--+++---+----++-+--+--++-++-+-/ |  | || | |  |  |  ||  |||| |||||      ||||||  | || | |    || ||  ||
|  | |||  ||| || |||| |    ||| | |   ||||||   || |  |||   |    || |  | /++-++-+---+--+-++-+-+--+--+--++--++++-+++++------++++++--+-++-+-+---\|| ||  ||
|  | |||  ||| || |||| |    ||| | |   ||||||   || |  |||   |    || |  | ||| ||/+---+--+-++-+-+--+--+\ ||  |||| |||||      ||||||  | || | |   ||| ||  ||
|  | |||  ||| || |||| |    ||| | | /-++++++---++-+--+++---+----++-+--+-+++-++++---+--+-++-+-+--+--++-++--++++-+++++------++++++--+-++-+-+---+++\||  ||
|  | |||  |||/++-++++-+----+++-+-+-+-++++++---++-+--+++---+----++-+--+-+++-++++---+--+-++-+-+--+--++-++--++++-+++++--\   ||||||  | || | |   ||||||  ||
|  | |||  |||||| |||| |   /+++-+-+-+-++++++-\ || |  |||   |    \+-+--+-+++-++++---+--+-++-+-+--+--++-++--++++-++/||  |   ||||||  | || | |   ||||||  ||
|  | |||  |||||| |||| |   |||| | | | \+++++-+-++-+--+++---+-----+-+--+-+++-++++---+--+-+/ | |  |  || ||  |||| || ||  |   ||||||  | || | |   ||||||  ||
|  | |||  |||||| |||| \---++++-+-+-+--+++++-+-++-+--+++---+-----+-+--+-+++-++++---+--+-+--+-+--+--++-++--++++-++-++--+---+++++/  | || | |   ||||||  ||
|  | |||  |||||| ||||     |||| | | |  ||||| | || |  |||   |     | |  | ||| ||||   |  | |  | |  |  || |\>-++++-++-++--+---++++/   | || | |   ||||||  ||
|  | |||  |||||| ||\+-----++++-+-+-+--+++++-+-++-/  |||   |     | |  | ||| ||||   |  | |  | |  |  || |   |||| || ||  |   ||||    | || | |   ||||||  ||
|  | |||  |||||| || |     ||\+-+-+-+--+++++-+-++----+++---+-----+-+--+-+++-++++---+--+-+--+-+--+--++-+---++++-++-/|  |   ||||    | || | |   ||||||  ||
|  | |\+--++++++-++-/     || | | | |  ||||| | ||    |||   |     | |  | ||| ||||   |  | |  | |  |  || |   \+++-++--+--+---++++----+-/| | |   ||||||  ||
|  \-+-+--++++++-++-------++-+-+-+-+--+++++-+-++----+++---+-----+-+--+-+++-/|||   |  | |  | |  |  || |    ||| ||  |  |   ||||    |  | | |   ||||||  ||
|    | |  |||||| ||       || | | | |  ||\++-+-++----+++---+-----+-+--+-+++--+++---+--+-+--+-+--+--++-+----+++-/|  |  |   ||||    |  | | |   ||||||  ||
|    | |  |||||| ||  /----++-+-+-+-+--++-++-+-++----+++---+--\  | |  | |||  |||   |  | |  | |  |  || | /--+++--+--+-\|   ||||    |  | | |   ||||||  ||
|    | |  |\++++-++--+----++-+-+-/ |  \+-++-+-++----+++---+--+--+-+--+-+++--+++---+--+-+--+-+--+--++-+-+--+++--+--+-++---++/|    |  | | |   ||||||  ||
|    \-+--+-++++-++--+----++-+-+---+---+-++-+-++----+++---+--+--+-+--+-+++--+++---+--+-+--+-+--/  || | |  |||  |  | ||   || |    |  | | |   ||||||  ||
|      |  | |||| ||  |    || | |   |   | || | ||    \++---+--+--+-+--+-+++--+++---+--+-+--+-+-----++-+-+--+++--+--+-++---/| |    |  | | |   ||||||  ||
|     /+--+-++++-++--+----++-+-+---+---+-++-+-++-----++---+--+--+-+--+-+++--+++---+-\| |  | |    /++-+-+--+++--+--+-++----+-+--\ |  | | |   ||||||  ||
\-----++--+-++++-++--+----++-+-+---+---+-/| | ||/----++---+--+--+-+-\| ||\--+++---+-++-+--+-+----+++-+-+--++/  |  | ||    | |  | |  | | |   ||||||  ||
      ||  | |||| ||  |    || | |   |   |  | | \++----++---+--+--+-+-++-++---+++---+-++-+--+-+----+++-+-+--++---+--+-++----+-/  | |  | | |   |||^||  ||
      ||  | |||\-++--+----++-+-+---+---+--+-+--++----++---+--+--+-+-++-++---+++---+-++-+--+-+----+++-+-+--+/   |  | ||    |    | |  | | |   ||||||  ||
      ||  | |||  ||  |    || | |   |   |  | |  ||    |\---+--+--+-+-++-++---+++---+-++-+--+-+----+++-+-+--+----+--+-++----+----+-+--+-+-+---++++++--/|
      ||  \-+++--++--+----++>+-+---+---+--+-+--++----+----+--+--+-+-++-++---+++---+-++-+--/ |    ||| | |  |    |  | ||    |    | |  | | |   ||||||   |
      ||    |||  ||  |    || | |   | /-+--+-+--++----+----+--+--+-+-++-++---+++---+-++-+----+----+++-+-+-\|    |  |/++----+----+-+--+-+\|   ||||||   |
      ||    |||  ||  |    || | |   | | |  | |  ||    |    |  |  | | ||/++---+++---+-++-+----+\   ||| | | ||    |  ||||    |    | |  | |||   ||||||   |
      ||    |||  ||  |    || | |   | | |  | |  ||    |    |  |  | | |||||   |||   | || |    ||   ||| | \-++----+--++/|    |    | |  | |||   ||||||   |
      ||    |||  ||  |    || | |   | | \--+-+--++----+----+--+--+-+-+++++---+++---+-++-+----++---+++-+---++----+--++-+----+----+>+--+-+++---++++/|   |
      ||    |||  ||  |    || | |   | |    | |  \+----+----+--+--+-+-++++/   |\+---+-++-+----++---++/ |   ||    |  || ^    |    | |  | |||   |||| |   |
      ||    |||  |\--+----++-+-+---+-+----+-+---+----+----+--+--+-+-++++----+-+---+-++-+----++---++--+---++----+--/| |    |    | |  | |||   |||| |   |
      ||    |||  |   |    || | |   | |    | |   |    |    |  |  | | |||\----+-+---+-++-+----++---++--+---++----+---+-+----+----+-+--+-+++---/||| |   |
      ||    |||  |   |    || \-+---+-+----+-+---+----+----+--+--+-+-+++-----+-+---+-++-+----++---++--+---++----+---+-+----+----+-+--/ |||    ||| |   |
      ||    |||  \---+----++---+---+-+----+-+---+----/    |  |  |/+-+++-----+-+---+-++-+----++---++--+---++----+---+-+----+----+-+----+++----+++-+\  |
      ||    |||      |    ||   |   | \----+-+---+---------+--+--+++-+++-----+-+---+-++-+----++---++--+---/|    |   | |    |    | |    |||    ||| ||  |
      ||    |||      |    ||   |   |      | |   |         |  |  ||| |\+-----+-/   | || |    ||   ||  |    |    |   | |    |    | |    |||    ||| ||  |
      ||    |||      |    ||   |   |      | |   |         |  |  ||| | |     |     | || |    ||   ||  \----+----/   | |    |    | |    |||    ||| ||  |
      |\----+++------+----++---+---+------+-+---+---------+--+--/|\-+-+-----+-----+-++-+----++---++-------+--------+-+----+----+-+----+++----+++-++--/
      | /---+++---\  |    ||   |   |      | |   |         |  |   |  | |     |     | || |    ||   ||       |        | |    |    | |    |||    ||| ||   
      | |   |||   |  |    ||   \---+------/ |   |         |  |   |  | |     |     \-++-+----++---++-------+--------+-+----+----+-/    |||    ||| ||   
      | |   |||   |  |    ||       |        |   |         |  |   |  | \-----+-------++-+----+/   ||       |        | |    \----+------++/    ||| ||   
      | |   |||   |  |    ||       |        |   |         \--+---+--+-------+-------++-+----+----++-------+--------+-+---------+------++-----+++-/|   
      | |   |\+---+--+----++-------+--------+---+------------+---+--+-------+-------++-+----+----++-------+--------+-/         |      ||     |||  |   
      | |   | |   |  |    ||       |        |   \------------+---+--/       |       || |    |    ||       |        |           |      ||     |||  |   
      | |   | |   |  |    |\-------+--------+----------------+---+----------+----->-++-+----+----++-------+--------+-----------+------/|     |||  |   
      | |   | |   |  |    |        |        |                |   |          \-------++-+----/    ||       |        \-----------+-------/     |||  |   
      | |   | \---+--+----+--------+--------+----------------+---+------------------+/ |         \+-------+--------------------/             |||  |   
      | |   \-----+--+----+--------+--------+----------------+---+------------------+--+----------/       |                                  |||  |   
      | |         |  |    |        \--------+----------------+---+------------------+--+------------------+--------------------------<-------++/  |   
      | |         |  \----+-----------------+----------------/   \------------------+--+------------------+----------------------------------++---/   
      | |         |       |                 |                                       |  \------------------+----------------------------------/|       
      | |         |       \-----------------/                                       |                     |                                   |       
      \-+---------+-------------------------------------------------------->--------/                     \-----------------------------------/       
        \---------/                                                                                                                                   """ 
try:
  track=input.split('\n')
  carts=[]
  Ysize=len(track)
  Xsize=len(track[0])
  directions='^>v<'
  dirLen=4
  turnLen=3
  #add carts - x,y, direction, last symbol
  for y in range(Ysize):
    for x in range(Xsize):
      if track[y][x] in directions:
      #all possible situations
        if x==0: #leftmost
          if y==0:
            lastDir='/'
          elif y==Ysize-1:
            lastDir='\\'
          elif track[y+1][x]==' ':
            lastDir='\\'
          elif track[y-1][x]==' ':
            lastDir='/'
          else:
            lastDir='|'
        elif x==Xsize-1: #rightmost
          if y==0:
            lastDir='\\'
          elif y==Ysize-1:
            lastDir='/'
          elif track[y+1][x]==' ':
            lastDir='/'
          elif track[y-1][x]==' ':
            lastDir='\\'
          else:
            lastDir='|'
        elif y==0: #highest
          if track[y][x-1]==' ':
            lastDir='/'
          elif track[y][x+1]==' ':
            lastDir='\\'
          else:
            lastDir='-'
        elif y==Ysize-1: #lowest
          if track[y][x-1]==' ':
            lastDir='\\'
          elif track[y][x+1]==' ':
            lastDir='/'
          else:
            lastDir='-'
        #intersection
        elif (not(track[y][x+1]==' ' or track[y][x-1]==' ' or track[y-1][x]==' ' or track[y+1][x]==' ')\
        and  (not track[y][x+1]==track[y-1][x]) and (not track[y][x-1]==track[y+1][x])):
          lastDir='+'
        #bar
        elif not (track[y][x+1]==' ' or track[y][x-1]==' '):
          lastDir='|'
        #dash
        elif not (track[y+1][x]==' ' or track[y-1][x]==' '):
          lastDir='-'
        elif( (not (track[y][x+1]==' ' or track[y+1][x]==' ')) or (not (track[y][x-1]==' ' or track[y-1][x]==' '))):
          lastDir='/'
        elif( (not (track[y][x-1]==' ' or track[y+1][x]==' ')) or (not (track[y][x+1]==' ' or track[y-1][x]==' '))):
          lastDir='\\'
        else:
          raise Exception('impossible situation found')
        carts.append([x,y,track[y][x],lastDir,0]);
  cartsLen=len(carts)
  #tick
  ayy=0
  location=colCart1=colCart2=colX=colY=flag=0
  while(8):
    if flag:
      location=str(colX)+","+str(colY)
      print "collision at "+location,". Removing carts",colCart1,colCart2
      dirAtCollision=carts[colCart1][3]
      if dirAtCollision in directions:
        dirAtCollision=carts[colCart2][3]
      track[colY]=track[colY][:colX]+dirAtCollision+track[colY][colX+1:]
      carts.pop(max(colCart1,colCart2))
      carts.pop(min(colCart1,colCart2))
      cartsLen=len(carts)
    if cartsLen<2:
        location=str(carts[0][0])+","+str(carts[0][1])
        raise Exception("last cart standing at "+location)
    flag=0
    ayy+=1
    carts=sorted(carts, key=op.itemgetter(1,0)) #movement order
    for cart in range(cartsLen):
      cartX,cartY, cartDir, cartLastDir=carts[cart][0],carts[cart][1],carts[cart][2],carts[cart][3]
      cartLastTurn=carts[cart][4]
      # check collision
      for cart2 in range(cartsLen):
        if (cart2==cart):
          continue
        if (cartX == carts[cart2][0] and cartY == carts[cart2][1]):
          flag=1
          colCart1=cart
          colCart2=cart2
          colX=cartX
          colY=cartY
          break
      if flag and (cart==colCart1 or cart==colCart2):
        continue
      
      #advance
      track[cartY]=track[cartY][:cartX]+cartLastDir+track[cartY][cartX+1:]
      #1
      if cartDir=='>':
        cartLastDir=track[cartY][cartX+1]
        if track[cartY][cartX+1]=='+':
          cartDir=directions[(directions.index(cartDir)+cartLastTurn-1)%dirLen]
          cartLastTurn=(cartLastTurn+1)%turnLen
        elif track[cartY][cartX+1]=='/':
          cartDir='^'
        elif track[cartY][cartX+1]=='\\':
          cartDir='v'
        elif track[cartY][cartX+1]==' ':
          raise Exception("cart " + str(cart) + " hit a space")
        else:
          pass
        # track[cartY][cartX+1]=cartDir
        track[cartY]=track[cartY][:cartX+1]+cartDir+track[cartY][cartX+2:]
        cartX+=1
      
      #2
      elif cartDir=='<':
        cartLastDir=track[cartY][cartX-1]
        if track[cartY][cartX-1]=='+':
          cartDir=directions[(directions.index(cartDir)+cartLastTurn-1)%dirLen]
          cartLastTurn=(cartLastTurn+1)%turnLen
        elif track[cartY][cartX-1]=='/':
          cartDir='v'
        elif track[cartY][cartX-1]=='\\':
          cartDir='^'
        elif track[cartY][cartX-1]==' ':
          raise Exception("cart " + str(cart) + " hit a space")
        else:
          pass
        track[cartY]=track[cartY][:cartX-1]+cartDir+track[cartY][cartX:]
        cartX-=1
        
      #3
      elif cartDir=='^':
        cartLastDir=track[cartY-1][cartX]
        if track[cartY-1][cartX]=='+':
          cartDir=directions[(directions.index(cartDir)+cartLastTurn-1)%dirLen]
          cartLastTurn=(cartLastTurn+1)%turnLen
        elif track[cartY-1][cartX]=='/':
          cartDir='>'
        elif track[cartY-1][cartX]=='\\':
          cartDir='<'
        elif track[cartY-1][cartX]==' ':
          raise Exception("cart " + str(cart) + " hit a space")
        else:
          pass
        track[cartY-1]=track[cartY-1][:cartX]+cartDir+track[cartY-1][cartX+1:]
        cartY-=1
          
      #4
      elif cartDir=='v':
        cartLastDir=track[cartY+1][cartX]
        if track[cartY+1][cartX]=='+':
          cartDir=directions[(directions.index(cartDir)+cartLastTurn-1)%dirLen]
          cartLastTurn=(cartLastTurn+1)%turnLen
        elif track[cartY+1][cartX]=='/':
          cartDir='<'
        elif track[cartY+1][cartX]=='\\':
          cartDir='>'
        elif track[cartY+1][cartX]==' ':
          raise Exception("cart " + str(cart) + " hit a space")
        else:
          pass
        track[cartY+1]=track[cartY+1][:cartX]+cartDir+track[cartY+1][cartX+1:]
        cartY+=1
        
      #5
      else:
        raise Exception("bad cartDir")
      
      #update cart
      carts[cart]=[cartX,cartY,cartDir,cartLastDir,cartLastTurn]
except Exception as e:
  print str(e),sys.exc_info()[2].tb_lineno
finally:
  raw_input()