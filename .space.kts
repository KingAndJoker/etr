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
            // Start deployment
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
            tags("\$BRANCH", "\$DOCKER_TAG", "latest")
        }
    }

    parameters {
        secret("private-key", "{{ project:DEPLOYER_SSH_KEY }}")
    }

    host {
        fileInput {
            source = FileSource.Text("{{ private-key }}")
            localPath = "/root/.ssh/id_rsa.b64"
        }

        shellScript {
            interpreter = "/bin/bash"
            content = """
                export BRANCH=${'$'}(echo ${'$'}JB_SPACE_GIT_BRANCH | cut -d'/' -f 3)
                export DOCKER_TAG=${'$'}BRANCH-${'$'}JB_SPACE_EXECUTION_NUMBER
                export DEPLOY_VERSION=${'$'}BRANCH.${'$'}JB_SPACE_EXECUTION_NUMBER

                # Create new deployment
                curl "https://dl-gsu-by.jetbrains.space/api/http/projects/id:{{run:project.id}}/automation/deployments/start" \
                -d "{\"targetIdentifier\": \"key:etr-container\", \"version\": \"${'$'}DEPLOY_VERSION\", \"commitRefs\": [{\"repositoryName\": \"{{run:git-checkout.repositories}}\", \"branch\": \"{{ run:git-checkout.ref }}\", \"commit\": \"{{run:git-checkout.commit}}\"}]}" -X POST -H "Authorization: Bearer ${'$'}JB_SPACE_CLIENT_TOKEN"
                base64 -d </root/.ssh/id_rsa.b64 >/root/.ssh/id_rsa
                chmod 0600 /root/.ssh/id_rsa

                ssh -o StrictHostKeyChecking=no deploy@{{ project:DL_CONTAINERS_HOST }} -p {{ project:DL_CONTAINERS_HOST_SSH_PORT }} bash deploy-etr.sh ${'$'}DOCKER_TAG
                if [ $? -eq 0 ] 
                then 
                    export RES=finish
                else 
                    export RES=fail
                fi
                # Report deployment status
                curl "https://dl-gsu-by.jetbrains.space/api/http/projects/id:{{run:project.id}}/automation/deployments/${'$'}RES" \
                -d "{\"targetIdentifier\": \"key:etr-container\", \"version\": \"${'$'}DEPLOY_VERSION\", \"commitRefs\": [{\"repositoryName\": \"{{run:git-checkout.repositories}}\", \"branch\": \"{{ run:git-checkout.ref }}\", \"commit\": \"{{run:git-checkout.commit}}\"}]}" -X POST -H "Authorization: Bearer ${'$'}JB_SPACE_CLIENT_TOKEN"

            """
        }
    }

}
