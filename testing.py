def num_rushes(slope_height, rush_height_gain, back_sliding):
    rushes = [0]
    rush(rushes, 0, slope_height, rush_height_gain, back_sliding)
    return rushes[0]

def rush(rushes, current, slope, forward, back):
    if current >= slope:
        return
    elif current + forward >= slope:
        rushes[0] += 1
        return
    else:
        rushes[0] += 1
        rush(rushes, current + forward - back, slope, forward, back)

ans = num_rushes(100, 15, 7)
print(ans)