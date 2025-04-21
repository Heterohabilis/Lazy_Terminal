
import React, { useState } from 'react';
import { SendHorizontal, Paperclip, Mic } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

type ChatInputProps = {
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
};

const ChatInput = ({ onSendMessage, isLoading = false }: ChatInputProps) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t bg-chat-input-bg p-4 rounded-t-xl">
      <form onSubmit={handleSubmit} className="flex flex-col">
        <div className="relative">
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            className="min-h-[56px] w-full resize-none bg-white border-muted rounded-xl pr-24 shadow-sm focus:shadow-md transition-shadow"
            disabled={isLoading}
          />
          <div className="absolute bottom-2 right-2 flex space-x-1">
            <Button
              type="button"
              size="icon"
              variant="ghost"
              className="rounded-lg h-8 w-8 hover:bg-chat-button hover:text-accent-foreground"
            >
              <Paperclip className="h-4 w-4" />
              <span className="sr-only">Attach file</span>
            </Button>
            <Button
              type="button"
              size="icon"
              variant="ghost"
              className="rounded-lg h-8 w-8 hover:bg-chat-button hover:text-accent-foreground"
            >
              <Mic className="h-4 w-4" />
              <span className="sr-only">Voice input</span>
            </Button>
            <Button
              type="submit"
              size="icon"
              className="rounded-lg h-8 w-8 bg-primary text-primary-foreground hover:bg-chat-button-hover"
              disabled={!message.trim() || isLoading}
            >
              <SendHorizontal className="h-4 w-4" />
              <span className="sr-only">Send message</span>
            </Button>
          </div>
        </div>
        <div className="mt-2 text-xs text-center text-muted-foreground">
          Messages are processed with AI.
        </div>
      </form>
    </div>
  );
};

export default ChatInput;
