import { Card } from "./ui/card";
import { cn } from "../lib/utils";

interface GardenCardProps {
  name: string;
  plantCount: number;
  onClick: () => void;
  className?: string;
}

const GardenCard = ({ name, plantCount, onClick, className }: GardenCardProps) => {
  return (
    <Card 
      className={cn(
        "p-6 space-y-4 cursor-pointer hover:shadow-lg transition-shadow",
        className
      )}
      onClick={onClick}
    >
      <div>
        <h3 className="text-xl font-semibold text-garden-soil">{name}</h3>
      </div>
      <div className="text-sm text-garden-soil/60">
        {plantCount} {plantCount === 1 ? 'plant' : 'plants'}
      </div>
    </Card>
  );
};

export default GardenCard;