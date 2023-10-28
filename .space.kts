job("Run only on tags") {
    startOn {
        gitPush {
            anyTagMatching {
                +"v*"
            }
        }
    }

    kaniko {
        beforeBuildScript {
            // Create an env variable BRANCH,
            // use env var to get full branch name,
            // leave only the branch name without the 'refs/heads/' path
            content = """
                export BRANCH=${'$'}(echo ${'$'}JB_SPACE_GIT_BRANCH | cut -d'/' -f 3)
                export DOCKER_TAG=${'$'}BRANCH-${'$'}JB_SPACE_EXECUTION_NUMBER
                export GITHUB_PAT=${'$'}JB_SPACE_API_URL/${'$'}JB_SPACE_PROJECT_KEY
                case ${'$'}BRANCH in 
                    "master") export LATEST="latest" ;;
                    *)  export LATEST="test" ;;
                esac
            """
        }
        build {
            context = "."
            dockerfile = "Dockerfile"
            args["TARGET_BRANCH"] = "\$BRANCH"
        }
        push("dl-gsu-by.registry.jetbrains.space/p/main/containers/etr") {
            tags("\$DOCKER_TAG", "\$BRANCH")
        }
    }

    container("Start deployment", image = "alpine:3.18") {
        kotlinScript { api ->
            // create and start deployment
            api.space().projects.automation.deployments.start(
                project = api.projectIdentifier(),
                targetIdentifier = TargetIdentifier.Id("etr-container"),
                version = System.getenv("JB_SPACE_EXECUTION_NUMBER"),
                // sync the job and deployment states
                syncWithAutomationJob = true
            )
        }
    }

    parameters {
        secret("private-key", "{{ project:DEPLOYER_SSH_KEY }}")
    }

    host {
        fileInput {
            source = FileSource.Text("{{ private-key }}")
            localPath = "/root/.ssh/id_rsa"
        }

        shellScript {
            interpreter = "/bin/bash"
            content = """
                ssh -o StrictHostKeyChecking=no deploy@${'$'}DL_CONTAINERS_HOST -p ${'$'}DL_CONTAINERS_HOST_SSH_PORT bash deploy-etr.sh
            """
        }
    }

}
