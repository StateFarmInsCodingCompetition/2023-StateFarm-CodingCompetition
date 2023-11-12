export const central_uri = "http://ec2-18-119-129-148.us-east-2.compute.amazonaws.com:5000/";
export async function post(path, body) {
    return await fetch(central_uri + path, {
        method: "post",
        credentials: "include",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json",
        },
    });
}

export async function get(path, params) {
    let paramPath = path;
    if (Object.keys(params).length !== 0) {
        paramPath = paramPath + "?";
        Object.entries(params).forEach((entry, index) => {
            if (index !== 0) {
                paramPath = paramPath + "&";
            }
            paramPath = paramPath + entry[0] + "=" + entry[1];
        });
    }
    return await fetch(central_uri + paramPath, {
        method: "get",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
    });
}