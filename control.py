import sys
import ctypes
import sdl2
import sdl2.ext

AIM_DETILS = {
    'x': 400,
    'y': 300,
    'w': 10,
    'h': 10,
}

JOYSTICK_DEADZONE = 8000

def poll_aim(jaxis, rect) -> None:
    if jaxis.which == 0:
        if jaxis.axis == 0:
            # x-axis rotation
            if jaxis.value < -JOYSTICK_DEADZONE:
                rect.x -= 10
            elif jaxis.value > JOYSTICK_DEADZONE:
                rect.x += 10
            else:
                rect.x = 400 
        elif jaxis.axis == 1:
            # y-axis rotation
            if jaxis.value < -JOYSTICK_DEADZONE:
                rect.y -= 10
            elif jaxis.value > JOYSTICK_DEADZONE:
                rect.y += 10
            else:
                rect.y = 300


def draw_aim(renderer, rect) -> None:
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
    sdl2.SDL_RenderDrawRect(renderer, rect)
    sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
    sdl2.SDL_RenderPresent(renderer)



def run() -> None:
    sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

    joystick = sdl2.SDL_JoystickOpen(0)

    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"Space joystick",
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
            sdl2.SDL_WINDOW_OPENGL)

    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

    # draw_aim(renderer, 100, 100)

    if not window:
        print(sdl2.SDL_GetError())
        return -1

    context = sdl2.SDL_GL_CreateContext(window)

    print(f'num joysticks: {sdl2.SDL_NumJoysticks()}')

    """
    for j in enumerate(sdl2.SDL_NumJoysticks()):
        print(sdl2.SDL_JoystickName(j))
    """

    cursor = sdl2.SDL_Rect(**AIM_DETILS) 

    event = sdl2.SDL_Event()
    running = True
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
            elif event.type == sdl2.SDL_KEYDOWN:
                key = sdl2.SDL_GetKeyName(event.key.keysym.sym).decode("utf-8")
                if key == 'W':
                    cursor.y -= 10
                elif key == 'S':
                    cursor.y += 10
                elif key == 'A':
                    cursor.x -= 10
                elif key == 'D':
                    cursor.x += 10
                print(key)
            elif event.type == sdl2.SDL_JOYAXISMOTION:
                # TODO: look at docs to actually log x/y values
                poll_aim(event.jaxis, cursor)
                print(f'{event.jaxis.axis}:  {event.jaxis.value}')
        draw_aim(renderer, cursor)
        

if __name__ == "__main__":
    sys.exit(run())
