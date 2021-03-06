# setup public rsa keys to be allowed to ssh in
echo "# auto-generated by update-ssh-keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDHF4tSS10FBCVCMBb+SlF5+UaSLfllNdfDhtw1t2VYMze/pxuGETmfSF4D1legmP5CUAncRsw3Sq/tEUnjSq7IR1gnoBkIIXQ5AxJLHgPDjnYSwbU2+rB1UF/6pZrMqmcOaj3Kz7tcVvKjpIYE6eSXhVwixPHztLbrXEG/BTp91j43V8yUcrsTLmGWXyJBXBvrS9YdAGHQV5zaKf50hkhp0E04NE1YkgrtaUoXrh9mdyIl3psaoxZHPq3SFHJXpcMu2xhxxNaevDuCk8uTDnYIJVmyWY0hRqZlrFhkurOvQLJ9XIuN7SBs6+mDcCUdhEbH5RVRyY+OuzI2+kcUvz6uoZgrLtba5aWNyYrRrQBUFFZC+M3HM2PKJK3uFZ9TLCjVaJnF6Q7fV+VMNxrZd7of0BXJICgNPKdYX2fE6B96Wvbc6htl3WytzVg49yWRYQR7nuVPnrQ/B/oGNjoirFTGArRHTZPnSwRfdDcFtXaLmMk6WoxbgSxiQ+v3jeTz0u5QuAVML5pp+nVYddN74ZGBUFI1+gJjf4psy2PqpAVdwzVhChoDO3eB7+1bBrHq//Z0SP/ZLj6jOt+0FhOXCu/suZPYxcf9Gs0VynIvYCivRkQ/X4xIkzY5aCxaInNhEFUzCb6q+WAC5jXS2xGamKcOX6qkxeWRGy/tq7LoVuez/Q== martinwong327@gmail.com
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDa5UfZ/g9jjOfJDg06Szkz6PemslCdJw5Pjc8BztUkP/v8yU+fGhXAjzPvMpCDZYBh2DbQrKV0aK1NO/YFDq3KR+ewfSRJ5viQ3M3z0lj+0uyQWM8Jb72WTfrpxSrrClm0ZSRWiuWjJiDfuGNCi6TmO74Uq4Gd7fPsSmbM/XgOwNL3i2Sp8dnYEEixQWzqH1R3HRUHOynkhqTEUuFt/mWswm746jlkOp/iafm22mCm791UxXtJcNOUzytGJNdbuiKLE5JL+DK6ws1Va1kUXA2hKTKDLUMdBcx66hBYV0cA2tbIWRoVJmR+Voa2tNJcKYJNeFC1AdzyyuAba+ucoXyE9P2roIPtqmESABkwvNd44NsYrMUJKcGpnd2EQrekxiLsgIB1+GmthCZuEQ2eS5+L2ElsCB+1UEaNYyX9LmBuZsEHc6lMxP+mffNyis6gmq+Ofgj1AEk2R2YU4uXnUoauZxA+p+bqn5A+8yr2hO2ejWk5Zbk0V1zNjqESXWE8C2+jyacq0Dgepfy57qq8Zknv8d0j2y1nIan5h+7IwPEg5OgHYxKGyaDNlaeDuIPu4zkQsdI/mzzTnx1hekzi4EmQx6cdAjA9qzHJT1tsUwlwKOxTW0kg2vgtJjc7bPCMpOUWfmTcJY3zC8CsRgzVfF13bHreAR3q6dcLq/NWk8z5nQ== martinwong327@gmail.com
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCjVpqP/2g6BWEkljck/0JcFUSFzM8+jpD2eNwhqPbzGN7UTN8kM03nMycwwFuMlUBZifYsOfsEsBnJ5k2jsAYylaDczPnijWXKRWG9XudfHowIUgpJqMLl8zsb8RuP6ZBCV3Fql3gGz+Gu07Z2RsLwcrIgxs2nmzy58SGWyiMFU5bwMhuG0aCtnFL+d3swdn3FxtONS/4lovG9hy/CVheNI+MKHiqIOuezKLcOVD6v37T4hcBZ+58f+LpB2fWwKK2hfXxe73kIFcRyE+9AHwbU/iVGGhoifOluUatfJfRfgxxNriLUiojm0WD9/TDFuiX5LVB3oBKyMum74CyDuIkr martin@martin-Desktop
" >> /home/core/.ssh/authorized_keys

# install docker-compose on /opt/bin
mkdir -p /opt/bin
export DOCKER_COMPOSE_VERSION=`git ls-remote --tags git://github.com/docker/compose.git | awk '{print $2}' |grep -v "docs\|rc" |awk -F'/' '{print $3}' |sort -V |tail -n1`
curl -L https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` > /opt/bin/docker-compose
chmod +x /opt/bin/docker-compose

# setup influxdb folder
mkdir -p /home/core/influxdb
