export const state = () => ({
    project: null
})

export const mutations = {
    project(state, project) {
        state.project = project
    },
}