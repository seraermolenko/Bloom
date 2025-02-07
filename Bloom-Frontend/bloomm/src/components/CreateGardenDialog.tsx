import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "../components/ui/dialog";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { PlusCircle } from "lucide-react";
import { useState } from "react";


interface CreateGardenDialogProps {
  onCreateGarden: (name: string) => void;
}
const CreateGardenDialog = ({ onCreateGarden }: CreateGardenDialogProps) => {
  const [name, setName] = useState("");
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreateGarden(name);
    setName("");
  };
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button className="bg-garden-leaf text-white hover:bg-garden-leaf/90">
          <PlusCircle className="mr-2 h-4 w-4" />
          Create New Garden
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] bg-garden-cream">
        <DialogHeader>
          <DialogTitle className="text-garden-soil">Create a New Garden</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 mt-4">
          <div className="space-y-2">
            <label htmlFor="name" className="text-sm font-medium text-garden-soil">
              Garden Name
            </label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="border-garden-sage focus:border-garden-leaf"
              placeholder="My Beautiful Garden"
              required
            />
          </div>
          <Button 
            type="submit" 
            className="w-full bg-garden-leaf text-white hover:bg-garden-leaf/90"
          >
            Create Garden
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
};
export default CreateGardenDialog;