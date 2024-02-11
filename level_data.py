from constants import (
    BRICK_COLOR, TYPE, NORMAL, STRONG, BARRIER, SPACING, SPACE_SIZE,
    BLUE, GREEN, RED, YELLOW, ORANGE, PURPLE
)

LEVELS = {
    1: [
        [{TYPE: SPACING, SPACE_SIZE: 1070}],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}
         ],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}
         ],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}
         ]],
    2: [[{TYPE: SPACING, SPACE_SIZE: 1070}],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}
         ],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}
         ],
        [{TYPE: SPACING, SPACE_SIZE: 15},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: BARRIER, BRICK_COLOR: RED},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: NORMAL, BRICK_COLOR: BLUE},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: STRONG, BRICK_COLOR: GREEN},
         {TYPE: SPACING, SPACE_SIZE: 15}
         ]]
}