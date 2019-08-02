"""
This is the test module and supports all the ReST actions for the
'test' collection
"""

# 3rd party modules
import pkg_resources
from flask import make_response
# native modules
import logging
import platform
import socket
import git
import time
import json
# local modules
from tsuro.tsurobot import Tsurobot, play_game
import logging

logger = logging.getLogger(__name__)

config_file = "./config.json"
tsurobot = Tsurobot(config_file)


def get_info():
    """
    This function responds to a request for /info
    with a lists of application and system info

    : return:        json with a 'packages' array and 'other' string
    """

    packages_list = [d.project_name + "==" + pkg_resources.get_distribution(d.project_name).version
                     for d in pkg_resources.working_set]

    with open(config_file) as f:
        config = json.load(f)
    other = socket.gethostname() + " - " + platform.platform()

    return {'packages': packages_list, 'other': other, 'config':config}


def get_ack():
    """
    This function responds to a request for /ack
    with a lists of application and system info
    """

    return make_response('Tsuro ACK', 200)


def put_git_pull(branch_name):
    """
    This function responds to a request for /git and
    updates the Tsurobot with the latest from the given branch
    """
    # git pull origin [branch]
    g = git.Git('./')
    g.pull('origin', branch_name)
    repo = git.Repo('./')
    branch = repo.head.ref.name
    commit_id = str(repo.head.commit)
    commit_message = repo.head.commit.message
    response_message = f'Successful git pull on {branch} for commit {commit_id}: {commit_message}'
    logging.info(response_message)

    return make_response(response_message, 200)

def post_flip_polarity_left_wheel():
    """
    This function responds to a request for /flip_polarity_left_wheel/
    with a '200' upon successful configuration
    """
    tsurobot.back_wheels.calibrate_left_polarity()
    tsurobot.back_wheels.save_config()
    return make_response('Tsurobot left wheel polarity flipped', 200)

def post_flip_polarity_right_wheel():
    """
    This function responds to a request for /flip_polarity_left_wheel/
    with a '200' upon successful configuration
    """
    tsurobot.back_wheels.calibrate_right_polarity()
    tsurobot.back_wheels.save_config()
    return make_response('Tsurobot right wheel polarity flipped', 200)

def post_test_back_wheels():
    """
    This function responds to a request for /test_back_wheels/
    with a '200' upon successful startup
    """
    tsurobot.back_wheels.speed = 100
    tsurobot.back_wheels.forward()
    time.sleep(1)
    tsurobot.back_wheels.speed = 20
    time.sleep(1)
    tsurobot.back_wheels.speed = 50
    time.sleep(1)
    tsurobot.back_wheels.speed = 100
    time.sleep(1)
    tsurobot.back_wheels.stop()

    return make_response('Tsurobot back wheel test complete', 200)

def post_turning_offset(offset):
    """
    This function responds to a request for /turning_offset/
    with a '200' upon successfull adjustment
    """
    for _x in range(abs(offset)):
        if offset > 0:
            tsurobot.front_wheels.calibrate_left()
        if offset < 0:
            tsurobot.front_wheels.calibrate_right()
    tsurobot.front_wheels.save_config()
    return make_response('Tsurobot front wheel calibration complete. Offset is {0}'.format(str(tsurobot.front_wheels.turning_offset)), 200)

def post_test_front_wheels():
    """
    This function responds to a request for /test_front_wheels/
    with a '200' upon successful startup
    """
    tsurobot.front_wheels.turn_left()
    time.sleep(1)
    tsurobot.front_wheels.turn_straight()
    time.sleep(1)
    tsurobot.front_wheels.turn_right()
    time.sleep(1)
    tsurobot.front_wheels.turn_straight()

    return make_response('Tsurobot front wheel test complete', 200)

def post_test_vertical_view():
    """
    This function responds to a request for /test_vertical_view/
    with a '200' upon successful startup
    """
    # start_state = tsurobot.get_state()
    # tsurobot.camera.tilt_up()
    # time.sleep(1)
    # tsurobot.camera.to_position(expect_tilt=start_state.tilt)
    # time.sleep(1)
    tsurobot.camera.tilt_down()
    time.sleep(1)
    tsurobot.camera.tilt_up()
    return make_response('Tsurobot vertical view test complete', 200)


def post_test_horizontal_view():
    """
    This function responds to a request for /test_horizontal_view/
    with a '200' upon successful startup
    """
    tsurobot.camera.pan_left()
    time.sleep(1)
    tsurobot.camera.pan_right()
    return make_response('Tsurobot horizontal view test complete', 200)


def post_play_game(action):
    """
    This function responds to a request for /tsuro/launch_game
    with a '200' upon successful completion
    """
    play_game(tsurobot)

    return make_response('Tsuro game play complete', 200)
