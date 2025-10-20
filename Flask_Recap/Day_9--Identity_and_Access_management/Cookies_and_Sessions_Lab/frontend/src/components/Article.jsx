import React, { useEffect, useState } from 'react';
import { useParams } from "react-router-dom"
import ReactMarkdown from "react-markdown"

import PayWall from "./PayWall.jsx";
import { makeEmojiList } from "../utils/index.js";

const initialState = {
    article : null,
    error : null,
    status : "pending"
}

function Article() {
    const [{ article, error, status }, setState] = useState(initialState)
    const { id } = useParams()

    useEffect(() => {
        setState(initialState);
        fetch(`/articles/${id}`).then((res) => {
            if (res.ok){
                res.json().then((article) =>
                    setState({article, error: null, status: "resolved" })
                )
            } else {
                res.json().then((message) =>
                    setState({ article: null, error: message['message'], status: "rejected" })
                )
            }
        })
    }, [id]);

    if (status === "pending"){
        return <h1>Loading...</h1>
    }

    if (status === "rejected"){
        if (error === "Maximum pageview limit reached."){
            return <PayWall />
        } else {
            return <h1>{error}</h1>
        }
    }

    const { title, author, date, content, minutes_to_read } = article
    const emojis = makeEmojiList(minutes_to_read)

    return (
        <article>
            <h1>{title}</h1>
            <small>
                <p>
                    {date} • {emojis} {minutes_to_read} min read
                </p>
                <p>
                    <em> Written by {author}</em>
                </p>
                <ReactMarkdown>{content}</ReactMarkdown>
            </small>
        </article>
    );
}

export default Article;