import { Card } from "./ui/card";
import { cn } from "../lib/utils";


interface PlantCardProps {
    name: string;
    species: string;
    image: string;
    onClick: () => void;
    className?: string;
  }
  
  const PlantCard = ({ name, species, image, onClick, className }: PlantCardProps) => {
    return (
      <Card 
        className={cn(
          "group relative overflow-hidden animate-plant-grow cursor-pointer transition-all duration-300",
          "hover:scale-105 active:scale-95",
          className
        )}
        onClick={onClick}
      >
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />
        <img 
          src={image} 
          alt={name}
          className="w-full h-full object-cover aspect-square"
        />
        <div className="absolute bottom-0 left-0 right-0 p-4 z-20 text-white">
          <h4 className="font-semibold">{name}</h4>
          <p className="text-sm text-white/80">{species}</p>
        </div>
      </Card>
    );
  };
  
  export default PlantCard;