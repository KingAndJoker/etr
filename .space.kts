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
}
