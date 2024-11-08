import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
# Parse the XML file
tree = ET.parse('/ORCA-algorithm/task_examples/my_env_fixed_2_log.xml')

# Get the root element
root = tree.getroot()

def points_on_line(x1, y1, x2, y2):
    points = []
    
    # Calculate the differences in x and y coordinates
    dx = x2 - x1
    dy = y2 - y1
    
    # Determine whether the line is more horizontal or vertical
    is_steep = abs(dy) > abs(dx)
    
    # If the line is more vertical, swap x and y coordinates
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        
    # Swap the endpoints if necessary to ensure x1 < x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    # Recalculate the differences in x and y coordinates after swapping
    dx = x2 - x1
    dy = y2 - y1
    
    # Calculate the error term
    error = dx // 2
    
    # Determine the direction of y increment
    y_step = 1 if y1 < y2 else -1
    
    # Iterate over the x coordinates
    y = y1
    for x in range(x1, x2 + 1):
        # Add the point to the list, considering the swap
        points.append((y, x) if is_steep else (x, y))
        
        # Update the error term and y coordinate
        error -= abs(dy)
        if error < 0:
            y += y_step
            error += dx
    
    return points
# Now, you can access different elements and attributes of the XML document
# For example, to print the tag of the root element:
print("Root element tag:", root.tag)
resolution = 0.1
for child in root:
    print("Child tag:", child.tag, "attributes:", child.attrib)
log = root[-1]
robot_coords = []
human_coords = []
first_agent = log.find("agent[@id='0']")[0]
for i in range(len(first_agent)):
    x_coords = float(first_agent[i].get("xr"))
    y_coords = float(first_agent[i].get("yr"))
    robot_coords.append((x_coords, y_coords))
    # im[int(np.round(y_coords)),int(np.round(x_coords))] = [255,0,0]

first_agent = log.find("agent[@id='1']")[0]
for i in range(len(first_agent)):
    x_coords = float(first_agent[i].get("xr"))
    y_coords = float(first_agent[i].get("yr"))
    human_coords.append((x_coords, y_coords))
    # im[int(np.round(y_coords)),int(np.round(x_coords))] =  [0,255,0]
images = []
frames = 100
increment = len(robot_coords)//frames
im = 255*np.ones((64,64,3))
obstacles = root[1]
map_points = []
for obs in obstacles:
    for i in range(len(obs)-1):
        x1 = float(obs[i].get("xr"))
        y1 = float(obs[i].get("yr"))
        x2 = float(obs[i+1].get("xr"))
        y2 = float(obs[i+1].get("yr"))
        map_points += points_on_line(int(np.round(x1/resolution)), int(np.round(y1/resolution)), int(np.round(x2/resolution)), int(np.round(y2/resolution)))
    
for point in map_points:
    im[int(np.round(point[1])),int(np.round(point[0]))] = [0,0,0]
images = []
for i in range(frames):
    temp_im = im.copy()
    for point in robot_coords[i*increment:(i+1)*increment]:
        temp_im[int(np.round(point[1]/resolution)),int(np.round(point[0]/resolution))] = [255,0,0]
    for point in human_coords[i*increment:(i+1)*increment]:
        temp_im[int(np.round(point[1]/resolution)),int(np.round(point[0]/resolution))] = [0,255,0]
    
    image = Image.fromarray(temp_im.astype(np.uint8))
    images.append(image)
# To iterate over child elements of the root element:

# To access specific elements and attributes, you can use indexing:




image = Image.fromarray(im.astype(np.uint8))
image.save('/ORCA-algorithm/task_examples/my_env_2.gif', save_all=True, append_images=images, duration=100, loop=0)