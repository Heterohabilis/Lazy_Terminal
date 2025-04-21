import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github.css';
import 'katex/dist/katex.min.css';
import { BotIcon, UserIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

export type Message = {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
};

type ChatMessagesProps = {
  messages: Message[];
  isLoading?: boolean;
};

const ChatMessages = ({ messages, isLoading }: ChatMessagesProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);


  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-6 text-center">
        <div className="w-16 h-16 rounded-full bg-accent flex items-center justify-center mb-4">
          <BotIcon className="h-8 w-8 text-accent-foreground" />
        </div>
        <h3 className="text-xl font-medium mb-2">Welcome to SoftWhisper</h3>
        <p className="text-muted-foreground max-w-md">
          This is your elegant chat interface. Send a message to start a conversation.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col space-y-6 p-6">
      {messages.map((message) => (
        <div
          key={message.id}
          className={cn("flex items-start gap-3", {
            "justify-end": message.role === "user",
          })}
        >
          {message.role === "assistant" && (
            <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
              <BotIcon className="h-4 w-4 text-secondary-foreground" />
            </div>
          )}

          <div
            className={cn({
              "user-bubble": message.role === "user",
              "assistant-bubble": message.role === "assistant",
            })}
          >
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex, rehypeHighlight]}
            >
              {message.content}
            </ReactMarkdown>
          </div>

          {message.role === "user" && (
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
              <UserIcon className="h-4 w-4 text-primary-foreground" />
            </div>
          )}
        </div>
      ))}

      {isLoading && (
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
            <BotIcon className="h-4 w-4 text-secondary-foreground" />
          </div>
          <div className="assistant-bubble">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse" />
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse" style={{ animationDelay: "0.2s" }} />
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse" style={{ animationDelay: "0.4s" }} />
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
