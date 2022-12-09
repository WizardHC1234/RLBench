from collections import defaultdict
from typing import List, Tuple

import numpy as np
from pyrep.objects.dummy import Dummy
from pyrep.objects.joint import Joint
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.task import Task
from rlbench.backend.task import BimanualTask


colors = [
    ('green', (0.0, 0.5, 0.0)),
    ('blue', (0.0, 0.0, 1.0)),
    ('yellow', (1.0, 1.0, 0.0)),
    ('olive', (0.5, 0.5, 0.0)),
    ('purple', (0.5, 0.0, 0.5)),
    ('teal', (0, 0.5, 0.5)),
    ('black', (0.0, 0.0, 0.0)),
    ('white', (1.0, 1.0, 1.0)),
]

class HandoverItem(BimanualTask):
    #..todo:: extend to hand over {orange, blue, yellow} item

    def init_task(self) -> None:


        self.items = [Shape(f'item{i}') for i in range(3)]
        self.register_graspable_objects(self.items)

        self.waypoint_mapping = defaultdict(lambda: 'left')
        self.waypoint_mapping.update({'waypoint0': 'right', 'waypoint5': 'right'})


    def init_episode(self, index) -> List[str]:

        success_sensor = ProximitySensor('Panda_rightArm_gripper_attachProxSensor')


        color_name, color = colors[index]
        self.items[0].set_color(color)
        
        remaining_colors = colors.copy()
        remaining_colors.remove((color_name, color))
        np.random.shuffle(remaining_colors)

        for i, item in  enumerate(self.items):
            item.set_color(remaining_colors[i][1])


        self.register_success_conditions(
            [DetectedCondition(self.items[0], success_sensor)])
        
        return [f'bring me the {color_name} item',
                f'hand over the {color_name} object']

    def variation_count(self) -> int:
        return len(colors)

    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0, 0, - np.pi / 8], [0, 0, np.pi / 8]
