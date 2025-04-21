
import React from 'react';
import { Server, Activity, Settings, PenTool, MessageSquare, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

type SidebarButtonProps = {
  icon: React.ElementType;
  label: string;
  onClick?: () => void;
};

const SidebarButton = ({ icon: Icon, label, onClick }: SidebarButtonProps) => {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="h-12 w-12 rounded-xl hover:bg-sidebar-accent text-sidebar-foreground hover:text-sidebar-accent-foreground transition-all duration-200 mb-2"
            onClick={onClick}
          >
            <Icon className="h-5 w-5" />
            <span className="sr-only">{label}</span>
          </Button>
        </TooltipTrigger>
        <TooltipContent side="right" className="bg-white border border-gray-200 shadow-md">
          {label}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
};

const ChatSidebar = () => {
  return (
    <aside className="flex flex-col items-center py-6 w-20 bg-sidebar fixed top-0 left-0 bottom-0 border-r border-sidebar-border">
      <div className="flex flex-col items-center mb-auto">
        <div className="mb-8">
          <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold text-xl">
            C
          </div>
        </div>
        
        <SidebarButton icon={Server} label="Add Server" />
        <SidebarButton icon={Activity} label="Switch Model" />
        <SidebarButton icon={MessageSquare} label="Conversations" />
        <SidebarButton icon={PenTool} label="Customize" />
        <SidebarButton icon={Plus} label="More Features" />
      </div>
      
      <div className="mt-auto">
        <SidebarButton icon={Settings} label="Settings" />
      </div>
    </aside>
  );
};

export default ChatSidebar;
