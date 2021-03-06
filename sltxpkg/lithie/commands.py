import sltxpkg.config as sc
import sltxpkg.globals as sg
import sltxpkg.prompt as prompt
from sltxpkg.lithie.docker_mg import DockerCtrl
# TODO: get valid names


def install_ask_user():
    valid_profiles = ['tx-small', 'tx-default', 'tx-full']
    print("Please enter the profile you want. Valid names are:", valid_profiles)
    target = prompt.get(
        "Profile [{default}]", default=sg.configuration[sg.C_DOCKER_PROFILE]).lower()
    # TODO: do not exit, try anyway
    if target not in valid_profiles:
        sg.LOGGER.error("%s was not found in %s exiting for now",
                        valid_profiles, target)
        exit(1)

    install(target)


def install(target: str):
    docker_ctrl = DockerCtrl()
    docker_ctrl.update_img(target)


# TODO: clarify time in docker container as it is utc it must be the same as host!!!!

def compile():
    sc.assure_dirs()
    docker_ctrl = DockerCtrl()
    profile = sg.configuration[sg.C_DOCKER_PROFILE] if sg.args.profile is None else sg.args.profile
    sltx_command = "sltx -t " + str(sg.args.threads) + " "

    if sg.args.log:
        sltx_command += '--log '

    if sg.args.verbose:
        sltx_command += '--verbose: '

    if sg.args.quiet:
        sltx_command += '--quiet '

    if sg.args.config is not None:
        sltx_command += '--config "' + sg.args.config + '" '

    sltx_command += 'raw-compile '

    if sg.args.recipe is not None:
        sltx_command += '--recipe "' + sg.args.recipe + '" '

    if sg.args.extra_arguments is not None:
        sltx_command += '--args="' + " ".join(sg.args.extra_arguments) + '" '

    for dep in sg.args.extra_dependencies:
        # will extend the dict with 'new' ones
        # should work even better if sltx-source.yaml files are present in the targets
        sltx_command += '--dependency "' + dep + '" '

    sltx_command += " ".join(['"' + f + '"' for f in sg.args.files])

    sg.LOGGER.info("Running command in docker: " + sltx_command)
    docker_ctrl.run_in_container(sg.args.dock_as_root, profile, sltx_command)
