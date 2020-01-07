import numpy as np

obj = [
    [0, 0, 0, 0, 1], 
    [0, 1, 1, 0, 0], 
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0]
]
obj = np.array(obj)


shape = obj.shape
value = [
    [0, 0, 0, 0, 1], 
    [0, 1, 1, 0, 0], 
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0]
]
for i in range(shape[0]):
    for j in range(shape[1]):
        value[i][j] = [0.25, 0.25, 0.25, 0.25] # 위, 아래, 좌, 우
v = np.array(value)


def pi(a):
    for i in range(len(a)):
        if a[i] == np.nan:
            a[i] = 0
            
    s = np.sum(a)
    if s == 0:
        print('here')
    for i in range(len(a)):
        a[i] /= s
    return a

def get_pi(a):
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] = pi(a[i][j])
    return a



s_0 = (0, 0)
goal = (3, 4)
def action(s):
    # eps는 사전 설정
    ## s_next 생성
    if np.random.rand() > eps:
        return np.argmax(v[s])
    else:
        return np.random.choice([0, 1, 2, 3], p=v[s])
    
def state_map(s, a):
    s = list(s)
    if a == 0:
        s[0] -= 1
    elif a == 2:
        s[0] += 1
    elif a == 2:
        s[1] -= 1
    else:
        s[1] += 1
    return tuple(s)

def is_wall(s):
    return (0, 0) <= s <= obj.shape



def update(s, a, r, s_next, v):
    # lr, gamma 는 위에서 설정하기
    if s_next == goal:
        v[s][a] = v[s][a] + lr * (r - v[s][a])
    else:
        v[s][a] = v[s][a] + lr * (r + gamma*np.argmax(v[s_next])) - v[s][a]
        
    v[s] = pi(v[s])
    return v


def play(s):
    global v
    fail_hist = []
    hist = []
    
    while 1:
        hist.append(s)
        print(s)
        a = action(s)
        s_next = state_map(s, a)
        
        if (0 > s[0] or s[0] > 3) or (0 > s[1] or s[1] > 4) or obj[s] == 1: ## 가면 안되는 곳
            fail_hist.append((s, s_next))
            r = -1
            v = update(s, a, r, s_next, v)
            s_next = (0, 0)
            
        if s_next == goal: ## 도착
            r = 1
            v = update(s, a, r, s_next, v)
            break
        else: ## 갈곳이 남음
            r = 0
            v = update(s, a, r , s_next, v)
            
        s = s_next



lr = 0.1
eps = 0.5
gamma = 0.95
v = np.array(value)
play(s_0)